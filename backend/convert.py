# backend/convert.py
from bs4 import BeautifulSoup
from markdownify import markdownify as md


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


def convert_to_markdown(html: str) -> str:
    """
    Convert HTML string to clean Markdown using markdownify.

    Args:
        html (str): HTML input string.

    Returns:
        str: Markdown-formatted content.
    """
    return md(html, heading_style="ATX")
