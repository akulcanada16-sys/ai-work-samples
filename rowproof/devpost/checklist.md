---
status: approved
build_mode: fast
---
# Build checklist

## Slices

- [x] Create local-first app shell, privacy explanation, paste/file/sample input, and responsive layout.
- [x] Implement CSV parser, delimiter detection, audit rules, preview, and safe export boundary.
- [x] Add real built-in samples, automated edge-case tests, README, demonstration storyboard, and submission facts.
- [x] Run automated tests, production-style local server, and browser verification.

## Hands-on checkpoints

- [x] Core flow inspected with local examples: sample → audit report → preview → safe/paused export state.

## Final review

- [x] Confirmed the proof of concept is ready for external review based on the requested feature set and local verification.

## Code Tour and App Map

- [x] App map created at `devpost/app-map.html` with primary paths and a reusable verification practice.

## Revisions

- The original boundary was preserved: no cloud upload, account, external API, or automatic repair was added. Normalized export is paused for structural ambiguity rather than guessing.
