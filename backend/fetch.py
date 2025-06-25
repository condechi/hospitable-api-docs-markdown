# backend/fetch.py
import requests
from datetime import datetime

BASE_URL = "https://developer.hospitable.com/docs/public-api-docs"

def fetch_html(path: str) -> dict:
    """
    Fetch the full HTML for a given documentation path.

    Args:
        path (str): The relative path of the documentation page (e.g. "/authentication").

    Returns:
        dict: A dictionary with keys:
              - 'html': The HTML content of the page
              - 'timestamp': ISO8601 UTC timestamp of the fetch time
    """
    full_url = BASE_URL + path
    print(f"🔗 Fetching: {full_url}")
    response = requests.get(full_url)
    response.raise_for_status()
    return {
        "html": response.text,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
