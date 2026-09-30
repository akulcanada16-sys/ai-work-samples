# Verification record — September 30, 2026

Tested on Python 3.12.14, OpenCV 5.0.0 (wheel 5.0.0.93), NumPy 2.5.3, Linux x86_64.

- **29 pytest cases passed.** Reading geometry, quality/ambiguity/out-of-scale decisions, malformed inputs/calibration, token checks, Lambda routes, derived-only S3 writes, and storage-failure handling. S3 is mocked; these are not cloud integration tests.
- **128-case procedural evaluation executed.** Per-case evidence and limitations committed; no field-accuracy claim.
- **HTTP smoke passed against a real local server.** Health/UI, actual PNG requests and annotated JSON results for clean/read, high/review, blur, ambiguity, missing and dark captures.
- **Browser smoke passed.** Playwright 1.62.1 driving Chromium 138.0.7204.0; displayed reading, review, retake, real file-upload interaction, JSON evidence download, and 390px mobile layout checked. No page JavaScript errors observed; no horizontal overflow. Desktop/mobile screenshots included.
- **Exploratory public-domain photo tested and rejected.** No independently verified reading, no field-success claim.

The agent-browser daemon could not start in this execution environment, and Playwright's direct browser download failed. Verification used an npm-distributed Chromium binary instead; this infrastructure workaround is not an application requirement. The actual browser smoke completed successfully.

**Not completed:** Docker image build, SAM/CloudFormation lint in a deployment environment, actual AWS deployment/S3/CloudWatch integration, independent field validation, target-user task study, final team/video recording, contest registration and final submission. No credentials or demo access code are committed.
