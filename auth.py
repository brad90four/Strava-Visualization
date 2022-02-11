import os
from pathlib import Path

import requests
from dotenv import load_dotenv, set_key
from loguru import logger


path = Path(__file__)
parent = path.parent
dotenv_file = parent.joinpath(".env")
load_dotenv(dotenv_file)
logger.debug(f"{parent=}")

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")


refresh_url = "https://www.strava.com/api/v3/oauth/token"

refresh_data = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "refresh_token",
    "refresh_token": REFRESH_TOKEN,
}



def refresh_strava(refresh_data) -> None:
    logger.debug(f"{refresh_data=}")
    refresh_code = requests.post(refresh_url, data=refresh_data)
    logger.debug(f"{refresh_code=}")
    logger.debug(f"{refresh_code.status_code = }")
    access_code = refresh_code.json()["access_token"]
    set_key(dotenv_file, "ACCESS_CODE", access_code)
    if refresh_code.status_code == 200 and access_code is not None:
        logger.info("Successfully refreshed strava access.")


refresh_strava(refresh_data)
