# sqlite3 database recorder test
import sqlite3
from pprint import pprint

from endpoints import get_altitude, get_distance, get_latlong, get_time
from loguru import logger


def create_database():
    """Create the strava database.

    Returns:
        None
    """
    con = sqlite3.connect("strava_test.db")
    cur = con.cursor()
    cur.execute("Drop TABLE IF EXISTS strava")
    cur.execute(
        """CREATE TABLE strava
                (activity_id TEXT, distance REAL, time REAL, altitude REAL, lat_long BLOB)"""
    )
    con.commit()
    con.close()


def database_print(db_name: str):
    """Print the contents of a database.

    Args:
        db_name (str): The name of the database to print.

    Returns:
        None.
    """
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute("SELECT * FROM strava")
    pprint(cur.fetchall()[0:5])
    con.close()


def write_data(
    activity_id: str = None,
    dist_data: dict = None,
    time_data: dict = None,
    alt_data: dict = None,
    latlng_data: dict = None,
) -> None:
    """Write activity data to a sqlite3 database.

    Args:
        activity_id (str): The activity id to write.
        dist_data (dict): A dictionary of the distance data.
        time_data (dict): A dictionary of the time data.
        alt_data (dict): A dictionary of the altitude data.
        latlng_data (dict): A dictionary of the lat/long data.

    Returns:
        None
    """
    con = sqlite3.connect("strava_test.db")
    cur = con.cursor()
    cur.execute(
        "SELECT EXISTS(SELECT 1 FROM strava WHERE activity_id = ?)", (activity_id,)
    )
    activity_test = cur.fetchall()
    if activity_test[0][0] == 0:
        logger.debug(f"Activity ID not in database. Adding {activity_id = }")
        dist = dist_data["distance"]
        time = time_data["time"]
        alt = alt_data["altitude"]
        latlng = latlng_data["lat_long"]
        payload = [
            (activity_id, dist[i], time[i], alt[i], str(latlng[i]))
            for i in range(len(dist))
        ]
        cur.executemany("INSERT INTO strava VALUES (?, ?, ?, ?, ?)", payload)
        con.commit()
        con.close()
    else:
        print("Activity already exists")


def read_data(activity_id: str) -> dict[str]:
    """Read activity data from a sqlite3 database.

    Args:
        activity_id (str): The activity id to read.

    Returns:
        activity_data (dict): A dictionary of the activity data. The key is the acitivty ID
        and the values are a list of the data.
    """
    con = sqlite3.connect("strava_test.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM strava WHERE activity_id = ?", (activity_id,))
    activity_data = {activity_id: cur.fetchall()}
    con.close()
    print(f"{type(activity_data) = }")
    print(f"{activity_data.keys() = }")
    print([type(k) for k in activity_data.keys()])

    return activity_data


if __name__ == "__main__":
    # running code with single activity data
    activity = "6492923259"
    altitude = {"altitude": get_altitude(activity)}
    lat_long = {"lat_long": get_latlong(activity)}
    distance = {"distance": get_distance(activity)}
    time = {"time": get_time(activity)}

    # todo create new table for setup

    # write_data(activity, distance, time, altitude, lat_long)
    # print(f"{'-'*5}After writing data{'-'*5}")
    # database_print("strava_test.db")

    # print(f"{'-'*5}After reading data{'-'*5}")
    # read_data("6492923259")
    # database_print("strava_test.db")

    print(read_data("123456"))
    print(len(read_data("123456")["123456"]))
