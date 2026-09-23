---
status: approved
---
# RowProof scope

## The problem

People often treat a CSV as plain text until it breaks an import, shifts a report, duplicates a record, or behaves unexpectedly in a spreadsheet. The damage is usually discovered after the file has been shared.

## Intended user

An operations worker, analyst, researcher, or small-team owner who receives or prepares a CSV and needs a fast, understandable preflight check without sending sensitive data to another service.

## The unique kernel

RowProof turns a CSV into a short, row-evidenced safety report in the browser, then only offers a normalized export when the file's structure supports a trustworthy reconstruction.

## Proof of success

A user can load a local CSV, see the detected delimiter, preview it accurately, identify a structural or spreadsheet-risk problem by row, and download an audit record. A well-structured file can also be downloaded with normalized headers and neutralized formula-like cells.

## In scope

- Paste and local file input.
- Comma, semicolon, tab, and pipe delimiter detection.
- Correct handling of doubled quotes, quoted delimiters, quoted newlines, and a final quoted-empty record.
- Findings for header, width, key, formula-prefix, control-character, and type-drift risks.
- Preview, JSON audit, and safe-only normalized CSV.
- Built-in test datasets and clear privacy explanation.

## Out of scope for this proof of concept

- Cloud storage, accounts, collaboration, server upload, analytics, and external APIs.
- Guessing repairs for malformed quotes or uneven rows.
- Domain-specific correctness rules, data enrichment, or automatic schema mapping.

## Why this is a small proof of concept

The app demonstrates one complete decision: whether a CSV is safe enough to normalize and pass on, with concrete evidence for the person making that decision.
