import os
import sys
from pathlib import Path

import requests

from dotenv import load_dotenv, set_key
from endpoints import get_athlete
from loguru import logger


def refresh_strava() -> None:
    """Refresh the access token if it has expired."""
    path = Path(__file__)
    parent = path.parent
    dotenv_file = parent.joinpath(".env")
    load_dotenv(dotenv_file)

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
    code = get_athlete()
    logger.debug(f"{code = }")
    if code == 401:
        logger.info("Access token has expired, will refresh acces token.")
        refresh_code = requests.post(refresh_url, data=refresh_data)
        logger.debug(f"{refresh_code.status_code = }")
        access_code = refresh_code.json()["access_token"]
        set_key(dotenv_file, "ACCESS_CODE", access_code)
        if refresh_code.status_code == 200 and access_code is not None:
            logger.info("Successfully refreshed strava access.")
        # time.sleep(5)
    elif code == 200:
        logger.info("Access token still valid.")
    else:
        logger.error(f"Strava API error: {code}")
        sys.exit(1)
