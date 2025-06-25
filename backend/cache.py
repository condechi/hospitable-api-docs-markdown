# backend/cache.py
import json
from pathlib import Path
from typing import Dict


def load_cache(cache_path: Path) -> Dict:
    """
    Load the cache JSON file if it exists, otherwise return an empty dictionary.

    Args:
        cache_path (Path): Path to scrape_cache.json

    Returns:
        dict: Cached HTML and timestamp info keyed by URL
    """
    if not cache_path.exists():
        return {}
    with cache_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_cache(cache: Dict, cache_path: Path):
    """
    Write the cache dictionary back to a file.

    Args:
        cache (dict): Dictionary to save
        cache_path (Path): Path to scrape_cache.json
    """
    with cache_path.open("w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)
        print(f"💾 Cache saved to {cache_path}")
