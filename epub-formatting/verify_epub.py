"""Structural checks for the generated EPUB; full validation requires EPUBCheck."""
from __future__ import annotations

from pathlib import Path
import re
from xml.etree import ElementTree as ET
from zipfile import ZIP_STORED, ZipFile

BOOK = Path(__file__).resolve().parent / "dist" / "an-index-of-small-things.epub"
CONTAINER_NS = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
OPF_NS = {"o": "http://www.idpf.org/2007/opf"}
XHTML_NS = {"x": "http://www.w3.org/1999/xhtml"}


def main() -> None:
    if not BOOK.is_file():
        raise SystemExit("Build the EPUB first: python build_epub.py")
    with ZipFile(BOOK) as book:
        names = book.namelist()
        assert names[0] == "mimetype", "mimetype must be the first archive item"
        assert book.getinfo("mimetype").compress_type == ZIP_STORED, "mimetype must be uncompressed"
        assert book.read("mimetype") == b"application/epub+zip", "mimetype content is incorrect"
        for required in ("META-INF/container.xml", "EPUB/package.opf", "EPUB/nav.xhtml"):
            assert required in names, f"missing required file: {required}"
        container = ET.fromstring(book.read("META-INF/container.xml"))
        rootfile = container.find(".//c:rootfile", CONTAINER_NS)
        assert rootfile is not None and rootfile.attrib.get("full-path") == "EPUB/package.opf", "container rootfile is incorrect"
        package = ET.fromstring(book.read("EPUB/package.opf"))
        manifest = {item.attrib["id"]: item.attrib["href"] for item in package.findall(".//o:manifest/o:item", OPF_NS)}
        assert manifest, "package manifest is empty"
        for href in manifest.values():
            assert f"EPUB/{href}" in names, f"manifest resource missing from archive: {href}"
        for itemref in package.findall(".//o:spine/o:itemref", OPF_NS):
            assert itemref.attrib["idref"] in manifest, "spine references an item outside the manifest"
        nav = ET.fromstring(book.read("EPUB/nav.xhtml"))
        links = nav.findall(".//x:a", XHTML_NS)
        assert len(links) >= 4, "navigation needs front matter and three chapter links"
        for link in links:
            href = link.attrib.get("href", "")
            if href.endswith(".xhtml"):
                assert f"EPUB/{href}" in names, f"navigation target missing: {href}"
        chapter_three = ET.fromstring(book.read("EPUB/chapter-03.xhtml"))
        assert chapter_three.find(".//*[@id='note-1']") is not None, "linked note target missing"
        story_words = 0
        for chapter in ("EPUB/chapter-01.xhtml", "EPUB/chapter-02.xhtml", "EPUB/chapter-03.xhtml"):
            document = ET.fromstring(book.read(chapter))
            body = document.find("x:body", XHTML_NS)
            assert body is not None, f"missing body in {chapter}"
            story_words += len(re.findall(r"\b[\w’'-]+\b", " ".join(body.itertext()), flags=re.UNICODE))
        assert 500 <= story_words <= 800, f"story word count outside requested range: {story_words}"
    print(f"Structural EPUB inspection passed; story word count: {story_words} (EPUBCheck not run).")


if __name__ == "__main__":
    main()
