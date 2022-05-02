# main strava script
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm, colors
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from database_test import read_data, write_data
from endpoints import (
    get_activities,
    get_altitude,
    get_athlete,
    get_distance,
    get_latlong,
    get_time,
    list_activities,
)
from loguru import logger


class NoActivityError(Exception):
    """Raised when the activity_id is not found in the database."""
    pass


def calc_speed(time_dict: dict, dist_dict: dict) -> dict:
    """Calculate speed between time and distance points."""
    speed = []
    time_delta = []
    dist_delta = []

    for i in range(len(time_dict) - 1):
        time_delta.append(time_dict[i + 1] - time_dict[i])

    for i in range(len(dist_dict) - 1):
        dist_delta.append(dist_dict[i + 1] - dist_dict[i])

    for t, d in zip(time_delta, dist_delta):
        speed.append((d / max(t, 1)) * 2.23694)  # m/s to mph

    speed.append(0)  # to handle the length change be calculating the deltas

    return speed


def latlng_to_feet(latlng: float) -> float:
    """Convert latitude or longitude to feet."""
    return latlng * 364488


def feet_to_latlng(feet: float) -> float:
    """Convert feet to decimal latitude / longitude."""
    return feet / 364488


def plotter(
    data: tuple[list[float], list[float], list[float]], speed: list, id_number: str
) -> None:
    """Function for plotting data in 3D"""
    logger.debug(f"Plotter starting for : {id_number}")
    X, Y, Z = data
    speed = speed
    x_lim = min(X), max(X)
    y_lim = min(Y), max(Y)
    z_lim = min(Z), max(Z)
    colormap_list = [
        "winter",
        "summer",
        "spring",
        "autumn",
        "viridis",
        "plasma",
        "hot",
        "gnuplot2",
        "cool",
        "bwr",
    ]
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection="3d")

    scaled_max = np.average(speed) + 2 * np.std(
        speed
    )  # max speed to be 2*std from average
    norm = colors.Normalize(vmin=0, vmax=scaled_max)

    ax.scatter(X, Y, Z, norm=norm, cmap="gnuplot2", c=speed, s=0.5)
    ax.set_zlim3d(z_lim)
    ax.set_box_aspect((1, 1, feet_to_latlng(1) * 100000))
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Altitude")
    ax.set_xticks(list(x_lim))
    ax.set_yticks(list(y_lim))
    ax.ticklabel_format(useOffset=False)
    fig.colorbar(
        cm.ScalarMappable(norm=norm, cmap="gnuplot2"),
        ax=ax,
        label="Speed in MPH",
        location="bottom",
        shrink=0.5,
    )
    # plt.show()

    ax.view_init(elev=90, azim=0)
    plt.savefig(f"{id_number}.png", dpi=300)
    ax.clear()
    plt.clf()
    plt.close()
    logger.debug("Plotter finished")


def animator(
    data: tuple[list[float], list[float], list[float]], speed: list, id_number: str
) -> None:
    """Animate a 3D plot based on the input data and save with the id_number."""
    logger.debug(f"Animator starting for : {id_number}")
    speed = speed
    X, Y, Z = data
    x_lim = min(X), max(X)
    y_lim = min(Y), max(Y)
    z_lim = min(Z), max(Z)
    colormap_list = [
        "winter",
        "summer",
        "spring",
        "autumn",
        "viridis",
        "plasma",
        "hot",
        "gnuplot2",
        "cool",
        "bwr",
    ]
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection="3d")

    scaled_max = np.average(speed) + 2 * np.std(
        speed
    )  # max speed to be 2*std from average
    norm = colors.Normalize(vmin=0, vmax=scaled_max)

    ax.scatter(X, Y, Z, norm=norm, cmap="gnuplot2", c=speed, s=0.5)
    ax.set_zlim3d(z_lim)
    ax.set_box_aspect((1, 1, feet_to_latlng(1) * 100000))
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Altitude")
    ax.set_xticks(list(x_lim))
    ax.set_yticks(list(y_lim))
    ax.ticklabel_format(useOffset=False)
    fig.colorbar(
        cm.ScalarMappable(norm=norm, cmap="gnuplot2"),
        ax=ax,
        label="Speed in MPH",
        location="bottom",
        shrink=0.5,
    )

    def init():
        ax.plot(X, Y, Z)
        return (fig,)

    def animate(i):
        ax.view_init(elev=30.0, azim=i)
        return (fig,)

    anim = FuncAnimation(
        fig, animate, init_func=init, frames=360, interval=20, blit=True
    )
    save_name = f"strava_vis_{id_number}.gif"
    anim.save(save_name, writer=PillowWriter(fps=30))
    # anim.save(save_name, writer=FFMpegWriter(fps=30))
    ax.clear()
    plt.clf()
    plt.close()
    logger.debug("Animator finished")


def main() -> None:
    """Command line interaction for listing activity, then plotting in 3D."""
    logger.debug("`main` starting")
    list_activities()
    activity = input("Enter target activity id: ")

    try:
        activity_data = read_data(activity)
        if len(activity_data[activity]) == 0:
            raise NoActivityError(f"No activity with id: {activity}")
        else:
            dist_data = []
            time_data = []
            alt_data = []
            lat_long_data = []

            for i in range(len(activity_data[activity])):
                dist_data.append(activity_data[activity][i][1])
                time_data.append(activity_data[activity][i][2])
                alt_data.append(activity_data[activity][i][3])
                lat, lon = (
                    activity_data[activity][i][4].strip("[").strip("]").split(",")
                )
                lat_long_data.append([float(lat), float(lon)])

            altitude = {"altitude": alt_data}
            distance = {"distance": dist_data}
            time = {"time": time_data}
            lat_long = {"lat_long": lat_long_data}
            speed = calc_speed(time_data, dist_data)

    except NoActivityError:
        altitude = {"altitude": get_altitude(activity)}
        lat_long = {"lat_long": get_latlong(activity)}
        distance = {"distance": get_distance(activity)}
        time = {"time": get_time(activity)}
        speed = calc_speed(time["time"], distance["distance"])
        write_data(activity, distance, time, altitude, lat_long)

    X = [x[1] for x in lat_long["lat_long"]]
    Y = [y[0] for y in lat_long["lat_long"]]
    Z = [z for z in altitude["altitude"]]
    animator((X, Y, Z), speed, activity)
    plotter((X, Y, Z), speed, activity)

    logger.debug("`main` finished")


def testing(debug_option: Optional[bool] = False) -> None:
    """Test `main` with a static activity ID."""
    logger.debug("Running test mode")
    activity_id = "6492923259"
    altitude = {"altitude": get_altitude(6492923259)}
    lat_long = {"lat_long": get_latlong(6492923259)}
    distance = {"distance": get_distance(6492923259)}
    time = {"time": get_time(6492923259)}

    speed_map = calc_speed(time["time"], distance["distance"])

    X = [x[1] for x in lat_long["lat_long"]]
    Y = [y[0] for y in lat_long["lat_long"]]
    Z = [z for z in altitude["altitude"]]

    if debug_option:
        x_lim = min(X), max(X)
        y_lim = min(Y), max(Y)
        z_lim = min(Z), max(Z)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot(X, Y, Z)
        ax.set_zlim3d(z_lim)
        ax.set_box_aspect((1, 1, feet_to_latlng(1) * 100000))
        ax.scatter(X, Y, Z, cmap="rainbow", c=speed_map)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_zlabel("Altitude")
        ax.set_xticks(list(x_lim))
        ax.set_yticks(list(y_lim))
        ax.ticklabel_format(useOffset=False)
        plt.show()
        x_lim = min(X), max(X)
        y_lim = min(Y), max(Y)
        z_lim = min(Z), max(Z)
        print(f"{X[:11] = }")
        print(f"{Y[:11] = }")
        print(f"{Z[:11] = }")
        print(f"{x_lim = }: {y_lim = }")
        print(f"x_range= {max(X) - min(X)}, y_range= {max(Y) - min(Y)}")
        print(f"{z_lim = }")
        print(f"z_range= {max(Z) - min(Z)}")
        print(f"{len(X) = }\n{len(Y) = }\n{len(Z) = }")

    write_data(activity_id, distance, time, altitude, lat_long)
    animator((X, Y, Z), "test", activity_id)
    plotter((X, Y, Z), "test", activity_id)

    logger.debug("`testing` finished")


def all_rides() -> None:
    """Plot all of the rides."""
    logger.debug("`all_rides` starting")
    all_activities = get_activities()
    for i in range(len(all_activities)):
        name = all_activities[i]["name"].replace(" ", "_")
        logger.debug(f"Making vis for {name}")
        activity = all_activities[i]["id"]
        altitude = {"altitude": get_altitude(activity)}
        lat_long = {"lat_long": get_latlong(activity)}
        X = [x[1] for x in lat_long["lat_long"]]
        Y = [y[0] for y in lat_long["lat_long"]]
        Z = [z for z in altitude["altitude"]]
        animator((X, Y, Z), name)

    logger.debug("`all_rides` finished")


if __name__ == "__main__":
    main()
    # testing(debug_option=False)
    # all_rides()
