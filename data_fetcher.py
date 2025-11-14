"""
Utility module responsible for fetching animal data from the
API Ninjas Animals API. Provides a single function `fetch_data`
that performs an HTTP request and returns parsed JSON results.
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()


REQUEST_URL = "https://api.api-ninjas.com/v1/animals"
API_KEY = os.getenv("API_KEY")
HEADERS = {"X-Api-Key": API_KEY}


def fetch_data(animal: str):
    """Fetch animal data from the API by name.

    Args:
        animal: The name to search (e.g., "Fox").

    Returns:
        A list of animals (each a dict) on success, or None on error.
    """
    try:
        res = requests.get(
            REQUEST_URL,
            headers=HEADERS,
            params={"name": animal},
            timeout=10,
        )
        if not res.ok:
            return None
        try:
            return res.json()
        except ValueError:
            return None
    except requests.RequestException:
        return None
