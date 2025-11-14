import requests
import os
from dotenv import load_dotenv
load_dotenv()


REQUEST_URL = "https://api.api-ninjas.com/v1/animals"
API_KEY = os.getenv('API_KEY')
HEADERS = {"X-Api-Key": API_KEY}


def fetch_data(animal: str):
    """
      Fetches the animal data for the animal 'animal_name'.
      Returns: a list of animals, each animal is a dictionary
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
