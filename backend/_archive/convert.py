import json
import sys
import re
import argparse
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from pathlib import Path

TOC_FILE = Path("toc_cache.json")
CACHE_FILE = Path("scrape_cache.json")
OUTPUT_FILE = Path("toc_updated.json")
BASE_URL = "https://developer.hospitable.com/docs/public-api-docs"

def load_json(file_path):
    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {} if file_path == CACHE_FILE else []

def save_json(data, path):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def extract_div(html):
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", {"class": "Editor"})
    return div.get_text(separator="\n", strip=True) if div else "[Missing div]"

def iso_to_toc_format(ts):
    """
    Convert a timestamp to ISO 8601 format with UTC timezone.
    """
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.isoformat(timespec="seconds") + "Z"
    except Exception:
        return ts

def is_stale(ts):
    """
    Check if a timestamp is older than 48 hours.
    """
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return datetime.now(timezone.utc) - dt > timedelta(hours=48)
    except Exception:
        return False

def fetch_html_with_playwright(url):
    """
    Fetch HTML content using Playwright to bypass server restrictions.
    """
    print(f"🔗 Fetching with Playwright: {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()
        page.goto(url, wait_until="networkidle")
        
        # Wait for the main content to load
        try:
            page.wait_for_selector('div[data-test="project-page"]', timeout=15000)
        except Exception as e:
            print(f"⚠️ Selector not found for {url}: {e}")
            browser.close()
            return None, None

        # Extract the HTML content
        html = page.content()
        timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds") + "Z"
        browser.close()
        return html, timestamp

def fetch_html(url):
    """
    Wrapper function to fetch HTML using Playwright.
    """
    full_url = BASE_URL + url
    html, timestamp = fetch_html_with_playwright(full_url)
    if html is None:
        raise Exception(f"Failed to fetch content from {full_url}")
    return html, timestamp

def main(fetch_missing=False, force=False):
    """
    Main function to sync TOC with scrape cache.

    Args:
        fetch_missing (bool): If True, fetch missing URLs and cache them.
        force (bool): If True, force fetching all TOC URLs and rebuild the cache.

    Returns:
        None
    """
    toc = load_json(TOC_FILE)
    cache = {} if force else load_json(CACHE_FILE)

    missing_urls = []
    stale_urls = []

    for item in toc:
        url = item.get("url")
        title = item.get("title")

        # Handle items without URLs
        if not url:
            item["content"] = title
            item["timestamp"] = datetime.now(timezone.utc).isoformat(timespec="seconds") + "Z"
            continue

        # Fetch content if necessary
        if force or fetch_missing and url not in cache:
            try:
                html, timestamp = fetch_html(url)
                cache[url] = {"html": html, "timestamp": timestamp}
                item["content"] = extract_div(html)
                item["timestamp"] = iso_to_toc_format(timestamp)
            except Exception as e:
                print(f"❌ Failed to fetch {url}: {e}")
                item["content"] = "[Error fetching]"
                item["timestamp"] = item.get("timestamp", "")
        elif url in cache:
            html = cache[url].get("html", "")
            item["content"] = extract_div(html)
            item["timestamp"] = iso_to_toc_format(cache[url]["timestamp"])
            if is_stale(cache[url]["timestamp"]):
                stale_urls.append(url)
        else:
            missing_urls.append(url)
            item["content"] = "[Missing from cache]"
            item["timestamp"] = item.get("timestamp", "")

    # Print summary of missing and stale URLs
    print("\n📌 Summary:")
    if missing_urls:
        print("🚫 Missing in cache:")
        for u in missing_urls:
            print(" -", u)
    if stale_urls:
        print("🕓 Stale cache entries (older than 48h):")
        for u in stale_urls:
            print(" -", u)

    # Save updated TOC and cache
    save_json(toc, OUTPUT_FILE)
    save_json(cache, CACHE_FILE)
    print(f"\n✅ TOC saved to {OUTPUT_FILE}")
    print(f"💾 Cache {'rebuilt' if force else 'updated'} and saved to {CACHE_FILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync TOC with scrape cache.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--fetch-missing", action="store_true", help="Fetch missing URLs and cache them.")
    group.add_argument("--force", action="store_true", help="Force fetching all TOC URLs and rebuild the cache.")
    args = parser.parse_args()

    main(fetch_missing=args.fetch_missing, force=args.force)
