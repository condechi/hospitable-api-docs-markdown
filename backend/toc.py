# backend/toc.py
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone  # Import timezone explicitly


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
        return datetime.now(timezone.utc) - dt > timedelta(hours=hours)
    except Exception:
        return False


def iso_to_toc_format(iso_ts: str) -> str:
    """
    Ensure the timestamp is in ISO8601 format.

    Args:
        iso_ts (str): Timestamp in ISO format.

    Returns:
        str: Timestamp in ISO8601 format.
    """
    try:
        dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
        return dt.isoformat() + "Z"  # Ensure 'Z' for UTC
    except Exception:
        return iso_ts  # fallback to raw if broken


def now_fmt() -> str:
    """
    Get the current UTC time in ISO8601 format.

    Returns:
        str: e.g., "2025-06-22T01:48:11+00:00Z"
    """
    return datetime.now(timezone.utc).isoformat(timespec="seconds") + "Z"
