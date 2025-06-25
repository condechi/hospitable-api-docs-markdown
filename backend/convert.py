# backend/convert.py
from bs4 import BeautifulSoup
from markdownify import markdownify as md_markdownify
import html2text
import mistune
import markdown
import commonmark
import markdown2
import pypandoc
from markdown_it import MarkdownIt
from markitdown import MarkItDown
import tempfile
import os

# Define available converters
def markitdown_converter(html: str) -> str:
    """
    Convert HTML to Markdown using MarkItDown.

    Args:
        html (str): HTML input string.

    Returns:
        str: Markdown-formatted content.
    """
    # Create a temporary file to store the HTML content
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
        temp_file.write(html.encode("utf-8"))
        temp_file_path = temp_file.name

    try:
        # Use MarkItDown to convert the temporary file to Markdown
        markdown = MarkItDown().convert(temp_file_path).text_content
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)

    return markdown


AVAILABLE_CONVERTERS = {
    "markdownify": lambda html: md_markdownify(html, heading_style="ATX"),
#    "html2text": lambda html: html2text.HTML2Text().handle(html),
    "markitdown": markitdown_converter,  # Updated to use the new function
    "markdown-it": lambda html: MarkdownIt().render(html),
#    "markdown2": lambda html: markdown2.markdown(html),
#    "python-markdown": lambda html: markdown.markdown(html),
#    "commonmark": lambda html: commonmark.commonmark(html),
#    "mistune": lambda html: mistune.create_markdown()(html),
#    "pandoc": lambda html: pypandoc.convert_text(html, "markdown", format="html"),
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
