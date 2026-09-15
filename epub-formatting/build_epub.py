"""Build the portfolio EPUB deterministically with Python's standard library."""
from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_STORED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source"
OUTPUT = ROOT / "dist" / "an-index-of-small-things.epub"
FIXED_TIMESTAMP = (2026, 9, 15, 0, 0, 0)


def archive_info(name: str, compression: int) -> ZipInfo:
    info = ZipInfo(name, FIXED_TIMESTAMP)
    info.compress_type = compression
    info.external_attr = 0o100644 << 16
    info.create_system = 3
    return info


def build() -> Path:
    files = sorted(path for path in SOURCE.rglob("*") if path.is_file() and path.relative_to(SOURCE).as_posix() != "mimetype")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT, "w") as book:
        book.writestr(archive_info("mimetype", ZIP_STORED), (SOURCE / "mimetype").read_text(encoding="ascii").strip().encode("ascii"))
        for path in files:
            name = path.relative_to(SOURCE).as_posix()
            # The sample is tiny. Storing each entry avoids zlib-version-dependent
            # bytes, so an Ubuntu CI rebuild can be compared to the committed EPUB.
            book.writestr(archive_info(name, ZIP_STORED), path.read_bytes())
    return OUTPUT


if __name__ == "__main__":
    print(build())
