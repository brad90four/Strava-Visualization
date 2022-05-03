# endpoints collection script
import os
from pathlib import Path

import requests

from dotenv import load_dotenv
from loguru import logger

load_dotenv(Path(__file__).parent.joinpath(".env"))
ACCESS_CODE = os.environ.get("ACCESS_CODE")


def get_athlete() -> None:
    """Get athlete data. Will only be used to test authentication."""
    athlete_url = "https://www.strava.com/api/v3/athlete"
    headers = {"accept": "application/json", "authorization": f"Bearer {ACCESS_CODE}"}
    response = requests.get(athlete_url, headers=headers)

    logger.debug(f"{response.status_code = }")
    return response.status_code


def get_activities() -> dict:
    """List athlete activities."""
    list_activities_url = "https://www.strava.com/api/v3/athlete/activities?per_page=30"
    headers = {"accept": "application/json", "authorization": f"Bearer {ACCESS_CODE}"}
    response = requests.get(list_activities_url, headers=headers)

    logger.debug(f"{response.status_code = }")
    return response.json()


def get_altitude(activity_id: str) -> dict[str, list[float]]:
    """Get altitude data from activity."""
    activity_stream = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=altitude&key_by_type=true"
    headers = {"accept": "application/json", "authorization": f"Bearer {ACCESS_CODE}"}
    response = requests.get(activity_stream, headers=headers)

    logger.debug(f"{response.status_code = }")
    return response.json()["altitude"]["data"]


def get_distance(activity_id: str) -> dict[str, list[float]]:
    """Get distance data from activity."""
    activity_stream = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=distance&key_by_type=true"
    headers = {"accept": "application/json", "authorization": f"Bearer {ACCESS_CODE}"}
    response = requests.get(activity_stream, headers=headers)

    logger.debug(f"{response.status_code = }")
    return response.json()["distance"]["data"]


def get_latlong(activity_id: str) -> dict[str, list[list[float, float]]]:
    """Get latitude and longitude from activity."""
    latlong_url = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=latlng&key_by_type=true"
    headers = {"accept": "application/json", "authorization": f"Bearer {ACCESS_CODE}"}
    response = requests.get(latlong_url, headers=headers)

    logger.debug(f"{response.status_code = }")
    return response.json()["latlng"]["data"]


def get_time(activity_id: str) -> dict:
    """Get time stamps from activity."""
    time_url = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=time&key_by_type=true"
    headers = {"accept": "application/json", "authorization": f"Bearer {ACCESS_CODE}"}
    response = requests.get(time_url, headers=headers)

    logger.debug(f"{response.status_code = }")
    return response.json()["time"]["data"]


def list_activities() -> dict:
    """List athlete activities."""
    list_activities_url = "https://www.strava.com/api/v3/athlete/activities?per_page=30"
    headers = {"accept": "application/json", "authorization": f"Bearer {ACCESS_CODE}"}
    response = requests.get(list_activities_url, headers=headers)

    logger.debug(f"{response.status_code = }")
    activities = response.json()
    for i in range(len(activities)):
        activity_id = activities[i]["id"]
        activity_description = activities[i]["name"]
        print(f"{activity_description : <35}: {activity_id}")
