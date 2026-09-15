"""Generate a browser-friendly HTML reading preview from the editable EPUB chapters."""
from __future__ import annotations

from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent
EPUB = ROOT / "source" / "EPUB"
OUTPUT = ROOT / "preview" / "reading-preview.html"
XHTML = "{http://www.w3.org/1999/xhtml}"


def tag_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def render(element: ET.Element, chapter_id: str) -> str:
    tag = tag_name(element.tag)
    attributes: list[str] = []
    for key, value in element.attrib.items():
        name = tag_name(key)
        if name == "type":  # EPUB semantics are retained in the ebook, not needed in HTML preview.
            continue
        if tag == "h1" and name == "id" and value == "chapter-title":
            value = chapter_id
        if tag == "section" and name == "aria-labelledby" and value == "chapter-title":
            value = chapter_id
        attributes.append(f' {name}="{escape(value, quote=True)}"')
    opening = f"<{tag}{''.join(attributes)}>"
    content = escape(element.text or "")
    for child in element:
        content += render(child, chapter_id) + escape(child.tail or "")
    return f"{opening}{content}</{tag}>"


def build() -> Path:
    css = (EPUB / "styles" / "book.css").read_text(encoding="utf-8")
    chapters = [
        ("chapter-01.xhtml", "chapter-01", "I. The Drawer"),
        ("chapter-02.xhtml", "chapter-02", "II. The Cards"),
        ("chapter-03.xhtml", "chapter-03", "III. The Missing Entry"),
    ]
    sections: list[str] = []
    links: list[str] = []
    for filename, chapter_id, title in chapters:
        document = ET.fromstring((EPUB / filename).read_bytes())
        body = document.find(f"{XHTML}body")
        if body is None or len(body) != 1:
            raise ValueError(f"Expected one content section in {filename}")
        links.append(f'<li><a href="#{chapter_id}">{escape(title)}</a></li>')
        sections.append(render(body[0], chapter_id))
    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>An Index of Small Things — reading preview</title><style>{css}</style></head>
<body><main><header class="title-page"><h1>An Index of Small Things</h1><p class="subtitle">Browser reading preview of the EPUB source</p></header>
<nav aria-label="Contents"><h2>Contents</h2><ol>{''.join(links)}</ol></nav>{''.join(sections)}</main></body></html>"""
    OUTPUT.write_text(document, encoding="utf-8", newline="\n")
    return OUTPUT


if __name__ == "__main__":
    print(build())
