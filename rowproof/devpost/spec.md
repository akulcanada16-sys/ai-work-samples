---
status: approved
---
# RowProof technical plan

## Platform and architecture

Static browser application with no build tooling or third-party runtime code. `index.html` supplies the accessible structure, `style.css` supplies responsive visual design, `src/app.js` connects interactions, and `src/csv-core.js` is the deterministic parsing, auditing, and export library. A tiny Node static server exists only to make local viewing convenient.

## Data flow

`File/text input → delimiter detection → state-machine parser → audit findings + preview → JSON / conditional CSV download`

The parser recognizes quoted field state, doubled quote escaping, line endings, embedded newlines, and terminal records. The auditor tracks exact source line positions and checks headers, widths, selected keys, formulas, control characters, and inferred types. Export uses RFC-style quote escaping and uses CRLF rows.

## Safety decision

The app permits normalized CSV only when parsing has no malformed quote and each data row matches the header width. It normalizes blank/duplicate header names and prefixes formula-like output values with an apostrophe. It never silently aligns or discards an uneven row.

## Verification approach

Node's built-in test runner exercises quoted-newline/quoted-empty preservation, header/width faults, identity and spreadsheet hazards, type drift, safe normalization, and output quoting. Browser verification checks the core input-to-report-to-download journey and narrow-screen layout.

## Run instructions

Run `npm start` and open `http://localhost:4173`. Run `npm test` for automated tests. No install step or credentials are required.
