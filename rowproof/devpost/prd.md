---
status: approved
---
# RowProof product requirements

## Core journey

1. The user lands on a calm page that states the privacy promise.
2. They paste CSV text, choose a local file, or select a built-in edge-case sample.
3. The audit runs immediately. The user may select a unique ID/email-like column as a key.
4. The report gives row-level findings, a compact count summary, detected delimiter, and a data preview.
5. The user downloads a JSON audit. If the structure is safe, they can also download a normalized CSV; otherwise the interface explains why that action is paused.

## Visual direction

Editorial and dependable rather than a generic developer dashboard: warm paper background, ink-colored type, strong serif headline, restrained blue action color, and amber/red evidence states. The report should feel like a careful field notebook, not an alarm wall.

## Accessibility and responsive behavior

- Use real labels, buttons, native selects, keyboard-operable controls, high-contrast text, and visible disabled state.
- On narrow screens, stack the hero, input controls, findings, and preview; preserve horizontal scrolling for wide data previews.
- Findings use text labels in addition to color.

## Important product behaviors

- State exactly that files stay in the browser and are not uploaded.
- Do not invent sample findings: samples must be actual CSV input run through the same audit.
- Preserve data in preview, including quoted newlines and empty quoted final fields.
- Flag a potential formula prefix; do not claim it definitely executes in every spreadsheet.
- Disable normalized export when malformed quoting or inconsistent row width makes a faithful structure uncertain.
