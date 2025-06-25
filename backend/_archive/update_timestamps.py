import json
from datetime import datetime
from pathlib import Path

TOC_FILE = Path("toc_cache.json")
CACHE_FILE = Path("scrape_cache.json")

def convert_to_iso8601_with_timezone(timestamp):
    """
    Convert a timestamp to ISO 8601 format with UTC timezone (e.g., 2025-06-21T08:01:18Z).
    """
    if isinstance(timestamp, int):  # Handle Unix timestamp in milliseconds
        try:
            dt = datetime.utcfromtimestamp(timestamp / 1000)  # Convert to seconds
            return dt.isoformat(timespec="seconds") + "Z"  # Append 'Z' for UTC
        except Exception as e:
            print(f"Error converting integer timestamp: {timestamp} - {e}")
            return timestamp

    if not isinstance(timestamp, str):
        print(f"Skipping non-string timestamp: {timestamp}")
        return timestamp  # Return the original value if it's not a string or int

    try:
        # Parse the timestamp and normalize to UTC
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return dt.isoformat(timespec="seconds") + "Z"  # Ensure 'Z' for UTC
    except ValueError:
        print(f"Invalid timestamp format: {timestamp}")
        return timestamp

def update_file_timestamps(file_path):
    """
    Update all timestamps in the given JSON file to ISO 8601 with UTC timezone.
    """
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Update timestamps in the TOC or cache
    if isinstance(data, list):  # TOC file
        for item in data:
            if "timestamp" in item:
                item["timestamp"] = convert_to_iso8601_with_timezone(item["timestamp"])
    elif isinstance(data, dict):  # Cache file
        for key, value in data.items():
            if "timestamp" in value:
                value["timestamp"] = convert_to_iso8601_with_timezone(value["timestamp"])

    # Save the updated data back to the file
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Updated timestamps in {file_path}")

def main():
    update_file_timestamps(TOC_FILE)
    update_file_timestamps(CACHE_FILE)

if __name__ == "__main__":
    main()