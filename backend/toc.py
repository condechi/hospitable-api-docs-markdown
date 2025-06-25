# backend/toc.py
import json
from pathlib import Path
from datetime import datetime, timedelta

TOC_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


def load_json(path: Path):
    """Safely load JSON from a file."""
    if not path.exists():
        return [] if path.name.startswith("toc") else {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path: Path):
    """Write JSON data to a file with UTF-8 encoding."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def is_stale(iso_ts: str, hours: int = 48) -> bool:
    """
    Check if a timestamp (ISO8601 string) is older than the given hours.

    Args:
        iso_ts (str): ISO8601 timestamp string (with 'Z')
        hours (int): Age threshold in hours

    Returns:
        bool: True if the timestamp is older than the threshold
    """
    try:
        dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
        return datetime.utcnow() - dt > timedelta(hours=hours)
    except Exception:
        return False


def iso_to_toc_format(iso_ts: str) -> str:
    """
    Convert ISO8601 timestamp to the TOC format (e.g., "2025-06-22 01:48:11").

    Args:
        iso_ts (str): Timestamp in ISO format.

    Returns:
        str: Timestamp in TOC-friendly format.
    """
    try:
        dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
        return dt.strftime(TOC_TIMESTAMP_FORMAT)
    except Exception:
        return iso_ts  # fallback to raw if broken


def now_fmt() -> str:
    """
    Get the current UTC time formatted in TOC timestamp style.

    Returns:
        str: e.g., "2025-06-22 01:48:11"
    """
    return datetime.utcnow().strftime(TOC_TIMESTAMP_FORMAT)
