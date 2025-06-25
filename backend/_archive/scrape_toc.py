import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

TOC_FILE = Path("toc_cache.json")
CACHE_FILE = Path("scrape_cache.json")

def load_json(file_path):
    """
    Load JSON data from a file.
    """
    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json(data, file_path):
    """
    Save JSON data to a file.
    """
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def fetch_html_with_selenium(url):
    """
    Fetch HTML content using Selenium with a visible Chrome browser.
    """
    print(f"🔗 Fetching: {url}")

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Start browser maximized

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Navigate to the URL
        driver.get(url)

        # Wait for the main content to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="project-page"]'))
        )

        # Extract the page source
        html = driver.page_source
        timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds") + "Z"
        return html, timestamp
    except Exception as e:
        print(f"⚠️ Failed to fetch content from {url}: {e}")
        return None, None
    finally:
        # Close the browser
        driver.quit()

def scrape_toc(limit=None):
    """
    Walk through the TOC file and scrape objects with a URL.
    """
    toc = load_json(TOC_FILE)
    cache = load_json(CACHE_FILE)

    scraped_count = 0

    for item in toc:
        url = item.get("url")
        if not url:
            continue

        if url in cache:
            print(f"✅ Skipping cached URL: {url}")
            continue

        # Fetch the content
        html, timestamp = fetch_html_with_selenium(url)
        if html:
            cache[url] = {"html": html, "timestamp": timestamp}
            print(f"✅ Fetched and cached: {url}")
        else:
            print(f"❌ Failed to fetch: {url}")

        scraped_count += 1
        if limit and scraped_count >= limit:
            print(f"🔒 Limit of {limit} reached. Stopping.")
            break

    # Save the updated cache
    save_json(cache, CACHE_FILE)
    print(f"💾 Cache saved to {CACHE_FILE}")

def main():
    parser = argparse.ArgumentParser(description="Scrape TOC URLs into a local cache.")
    parser.add_argument("--limit", type=int, help="Limit the number of objects to scrape.")
    args = parser.parse_args()

    scrape_toc(limit=args.limit)

if __name__ == "__main__":
    main()