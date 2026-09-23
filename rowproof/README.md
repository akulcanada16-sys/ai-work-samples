# RowProof

**CSV evidence, before the spreadsheet.** RowProof is a local-first browser tool that inspects a CSV before an analyst imports it, shares it, or opens it in spreadsheet software.

It detects delimiter and quoted-field edge cases, blank and duplicate headers, mismatched row widths, blank or duplicate values in a chosen key column, spreadsheet formula prefixes, hidden control characters, and type drift. It produces an evidence-rich report with row locations. When row structure is sound, it can download a normalized CSV and neutralize formula-like cells; otherwise it deliberately pauses the export.

## Why it matters

CSV files look simple and often fail silently. A stray line break can shift later columns, an empty identifier can misjoin records, and a cell beginning with `=` can run as a spreadsheet formula. RowProof gives operations teams, researchers, and small organizations a quick private gate before a file crosses a boundary.

## Privacy

All parsing and auditing happens in the browser. RowProof has no server endpoint for CSV data, no account, no analytics, and no external API. Closing or refreshing the tab clears the file from memory.

## Run locally

You need a current Node.js installation.

```bash
npm start
```

Then open `http://localhost:4173` in a browser. No dependency install is needed.

## Test

```bash
npm test
```

## Try the built-in examples

- **Clean contacts** — a baseline valid file.
- **Spreadsheet hazards** — duplicate and blank keys, a formula-like cell, and a hidden control character.
- **Quoted records** — a quoted newline, quoted delimiter, and final quoted-empty record.
- **Broken import** — duplicate headers, type drift, and a short row that blocks a clean export.

## Project materials

- [Planning and build record](devpost/)
- [Demo storyboard](DEMO.md)
- [Competition-ready project facts](SUBMISSION-NOTES.md)

## AI disclosure

This project was built during the Build With AI: Basics submission period with the Devpost Learn Skill Pack and a coding agent. The creator directed the project purpose, product constraints, and feature set; the agent assisted with implementation, testing, and documentation. The app uses no runtime AI model, external AI service, paid service, third-party API, or externally sourced user data.

## Limitations

RowProof is a proof of concept, not a replacement for domain-specific validation. Type checks are heuristic and infer from simple value patterns. It does not repair malformed quoted files or decide whether values are semantically correct. The normalized export is intentionally unavailable if an unclosed quote or mismatched row width makes a safe reconstruction ambiguous.
