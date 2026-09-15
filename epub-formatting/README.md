# An Index of Small Things — EPUB3 formatting sample

This is a small, original EPUB3 portfolio sample. It contains a fictional three-chapter story, **“An Index of Small Things,”** arranged as a reflowable ebook with front matter, a linked table of contents, a styled data table, an endnote link, and Unicode names.

It is a formatting sample, not client work, a published book, or a claim of retail/device compatibility. The story and all source files were produced with an AI coding agent under the owner's direction; there are no third-party images, fonts, or copied manuscript text.

## Files

- `source/` — editable EPUB source: XHTML, CSS, package document, navigation document, and container metadata.
- `build_epub.py` — deterministic standard-library build script.
- `build_preview.py` — standard-library generator for the browser reading preview.
- `dist/an-index-of-small-things.epub` — generated EPUB artifact.
- `preview/index.html` — browser landing page linking to the preview options.
- `preview/reading-preview.html` — generated, ordinary-HTML reading preview containing the same three chapters, navigation, table, and linked note as the EPUB source.
- `verify_epub.py` — local structural inspection; it is not a replacement for EPUBCheck.

## Build and inspect

From this folder, run:

```text
python build_epub.py
python verify_epub.py
```

The build writes `mimetype` first in the archive without ZIP compression, then writes the remaining files in a fixed sorted order and timestamp. This follows the EPUB Open Container Format packaging rule for the `mimetype` file. The small sample stores its other entries too, avoiding compression-library differences so an Ubuntu rebuild can be compared byte-for-byte with the committed EPUB. The source includes the required `META-INF/container.xml`, package document, manifest, spine, and EPUB3 navigation document.

`verify_epub.py` checks the resulting archive order and compression, required package files, XML well-formedness, manifest resources, spine references, navigation targets, and the linked note target. It does not claim full EPUB conformance.

## Validation status

The official validator is [EPUBCheck](https://www.w3.org/publishing/epubcheck/), a W3C project maintained by the DAISY Consortium. EPUBCheck 5.3.0 is the current production release listed by its official release notes and supports EPUB 3.3.

The public [GitHub Actions validation run 35030516318](https://github.com/akulcanada16-sys/ai-work-samples/actions/runs/35030516318) passed on 2026-09-15 for commit `9dac5447c288d33575eb79b07b0265288935f5a9`. It rebuilt the EPUB, confirmed its SHA-256 as `5e2796e5a4ffa6844320f0dd693e503c45e3dd542ee6ab04f7aea192b268d493`, verified the pinned EPUBCheck release archive, and reported:

```text
Validating using EPUB version 3.3 rules.
No errors or warnings detected.
Messages: 0 fatals / 0 errors / 0 warnings / 0 infos
EPUBCheck completed
```

This validates the packaged EPUB against EPUBCheck’s EPUB 3.3 rules. It does not claim testing in any particular ebook reader, device, store, or distribution service.

`integration/github-actions-epubcheck.yml` is an inactive template for the public repository. It downloads the official [EPUBCheck 5.3.0 release ZIP](https://github.com/w3c/epubcheck/releases/download/v5.3.0/epubcheck-5.3.0.zip), verifies SHA-256 `6c07e68584b2e2ce2f89fe06e1246dfead3eb36b46b340e7d93524f29dcff6c5`, builds this sample, runs the local structural check, and runs EPUBCheck with warnings treated as failures. The hash was calculated from that official release asset on 2026-09-15; the release page did not publish a separate checksum file. The template is not an executed validation result.

The packaging requirements used here are documented in the W3C [EPUB Open Container Format](https://www.w3.org/publishing/epub3/epub-ocf.html) and [EPUB Packages](https://www.w3.org/publishing/epub3/epub-packages.html) specifications.

## Inspection notes

- Run `python build_preview.py`, then open `preview/reading-preview.html` in a browser to inspect a standard-HTML reading preview without an ebook reader.
- The direct XHTML links remain available from `preview/index.html` as an editable-source inspection path; the generated HTML preview is the ordinary browser reading path.
- The table in Chapter Two is fictional research-card content, included only to demonstrate accessible table markup.
- The linked note in Chapter Three is a fictional editorial note. It is not a source citation.
- The e-book is intentionally reflowable and uses only system font families; no fixed-layout or device-specific behavior is claimed.
