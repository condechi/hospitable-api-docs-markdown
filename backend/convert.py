# backend/convert.py
from bs4 import BeautifulSoup
from markdownify import markdownify as md_markdownify
import html2text

# Define available converters
AVAILABLE_CONVERTERS = {
    "markdownify": lambda html: md_markdownify(html, heading_style="ATX"),
    "markitdown": lambda html: html2text.HTML2Text().handle(html),
}


def extract_main_div(html: str) -> str:
    """
    Extract the div with data-test="project-page" from the HTML.

    Args:
        html (str): Raw HTML document.

    Returns:
        str: Inner HTML of the main content div or placeholder.
    """
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", {"data-test": "project-page"})
    return str(div) if div else "<div>[Missing content]</div>"


def convert_to_markdown(html: str, converter: str) -> str:
    """
    Convert HTML string to Markdown using the selected converter.

    Args:
        html (str): HTML input string.
        converter (str): The Markdown converter to use (e.g., "markdownify", "markitdown").

    Returns:
        str: Markdown-formatted content.
    """
    if converter not in AVAILABLE_CONVERTERS:
        raise ValueError(f"Unsupported Markdown converter: {converter}")
    return AVAILABLE_CONVERTERS[converter](html)
