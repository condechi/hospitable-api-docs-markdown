# backend/main.py
import argparse
from pathlib import Path
from backend.fetch import fetch_html
from backend.toc import load_json, save_json, iso_to_toc_format, now_fmt
from backend.convert import extract_main_div, convert_to_markdown, AVAILABLE_CONVERTERS

# Define paths to source and output files
TOC_PATH = Path("toc_cache.json")
CACHE_PATH = Path("scrape_cache.json")
OUTPUT_PATH = Path("toc_updated.json")

def sync(fetch_missing=False, force=False, markdown_converter=None):
    """
    Syncs the TOC entries with cached or newly fetched documentation content.

    Args:
        fetch_missing (bool): If True, only fetch entries not in the cache.
        force (bool): If True, fetch all entries regardless of cache.
        markdown_converter (str or None): The Markdown converter to use (e.g., "markdownify", "markitdown").
                                           If None, all available converters will be used.

    Returns:
        None
    """
    toc = load_json(TOC_PATH)
    cache = {} if force else load_json(CACHE_PATH)

    for item in toc:
        url = item.get("url")
        title = item.get("title")

        # Initialize the versions object
        versions = {}

        # If URL is null, use the title as the default version
        if not url:
            versions["default"] = title
            item["versions"] = versions
            item["timestamp"] = now_fmt()
            continue

        # Determine whether we need to fetch content
        if force or (fetch_missing and url not in cache):
            try:
                res = fetch_html(url)
                html = res["html"]
                ts = res["timestamp"]
                cache[url] = {"html": html, "timestamp": ts}
            except Exception as e:
                print(f"❌ Failed to fetch {url}: {e}")
                continue

        # Extract and convert HTML to Markdown, update TOC item
        if url in cache:
            html = cache[url].get("html", "")
            ts = cache[url].get("timestamp", now_fmt())
            div_html = extract_main_div(html)

            # Add the default version as the raw HTML
            versions["default"] = div_html

            # Generate Markdown for all converters or a specific one
            converters_to_use = (
                [markdown_converter] if markdown_converter else AVAILABLE_CONVERTERS.keys()
            )
            for converter in converters_to_use:
                markdown = convert_to_markdown(div_html, converter)
                versions[converter] = markdown

            item["versions"] = versions
            item["timestamp"] = iso_to_toc_format(ts)

    # Save updated TOC and cache to disk
    save_json(toc, OUTPUT_PATH)
    save_json(cache, CACHE_PATH)
    print("✅ toc_updated.json and scrape_cache.json updated.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync TOC and scrape content.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--fetch-missing", action="store_true", help="Fetch only missing URLs.")
    group.add_argument("--force", action="store_true", help="Force fetch all URLs.")
    parser.add_argument(
        "--markdown-converter",
        choices=list(AVAILABLE_CONVERTERS.keys()),
        help="Select the Markdown converter to use. If not specified, all converters will be used."
    )
    args = parser.parse_args()

    sync(fetch_missing=args.fetch_missing, force=args.force, markdown_converter=args.markdown_converter)
