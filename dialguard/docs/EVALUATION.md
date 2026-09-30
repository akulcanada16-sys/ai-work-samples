# Evaluation evidence and limits

## Procedural suite

Run `python scripts/evaluate.py`. The committed JSON contains 128 cases, deterministic image seeds/hashes, ground-truth fixture values, status, errors, version/source identity and timings. The benchmark seed is 20260930. Interactive values (62/90) differ from benchmark random readings. Generator geometry and calibration are shared, so this is an implementation check, not an independently sampled external test set.

| Observation | First measured result |
|---|---:|
| Readable clean/noisy fixtures | 80 |
| Accepted readable fixtures | 79 (98.75%) |
| Mean absolute error among accepted | 0.557176 scale units on 0–100 |
| Maximum error among accepted | 0.811941 scale units |
| Invalid blurred/dark/missing/ambiguous fixtures | 48 |
| Invalid fixtures returning a reading | 0 |
| Clean fixtures incorrectly rejected | 1 / 40 |
| Noisy fixtures accepted | 40 / 40 |
| Longest-center-line Hough baseline detection on readable fixtures | 80 / 80 |
| Baseline error on readable fixtures | 1.428632° ≈ 0.529123 scale units |

The baseline is slightly more accurate and has higher readable coverage here. Do **not** market DialGuard as more accurate. Its candidate value is rejection of some poor captures, explicit review thresholds, observable decisions, and source evidence. A baseline line detection alone is not a trustworthy numeric reading; `baseline_invalid_detections_n` records how often it nevertheless produces a line in invalid fixtures. A proper field comparison must give both methods equivalent quality gates/calibration and report coverage plus conditional error.

The first local median was about 8 ms and p95 about 13 ms. Rerun timings vary. They exclude upload, AWS cold start, image-container startup and S3 writes; they are not service-level latency or cost measurements. Use the JSON from the actual run when reporting timing.

Thresholds and render parameters are developer-selected. No learned model, human-labeled test dataset, independent instrument readings, trained confidence calibration or statistical field confidence interval is claimed. Repeated development runs on the suite mean it is not a pristine holdout.

## Exploratory real photo

`evidence/air-pressure-gauge-tokino.jpg`: *Air pressure gauge*, Tokino, August 2006, public domain (PD-self), Wikimedia Commons. Source: https://commons.wikimedia.org/wiki/File:Air_pressure_gauge.jpg. Original file: https://upload.wikimedia.org/wikipedia/commons/a/a1/Air_pressure_gauge.jpg. The downloaded file's SHA1 matches the source record: `5c7ee0b63603f387170fbb7a25142ee6d3fd14ae`. The original photo is unmodified; the separate annotated derivative adds the calibration circle, detected ray and status.

Run `python scripts/evaluate_photo.py`. The photo is tilted and outside this version's supported scope. An exploratory manual hub/radius/scale specification yields RETAKE because the estimated angle lies outside the configured sweep. **This does not demonstrate reliable tilt detection.** There is no verified reading or instrument calibration. It is disclosed as one rejected natural-image case, not part of the numerical accuracy benchmark.

## Known failure modes

- Wrong hub, radius, scale, sweep or camera roll can produce a confidently supported wrong result.
- Text/graphics, a dark shadow, an unusually long counterweight, multiple needles or nonlinear scales can defeat ray assumptions. Some are rejected; others may be accepted incorrectly.
- The sharpness metric depends on resolution, contrast and surrounding markings; it can pass a blurred needle or reject a valid low-contrast image.
- Perspective tilt changes angle-to-value mapping; perspective rectification is not implemented.
- A diagnostic support of 1 does not imply 100% confidence. No automatic actuation or safety decision is allowed.

## Next field protocol

Collect rights-cleared original photographs from at least five different dark-needle/light-face linear gauges. Independently record instrument readings and scale endpoints rather than using this detector's output as truth. Include multiple values, lighting conditions and failure captures. Keep development/tuning gauges separate from at least two entirely held-out gauges; freeze code/gates/calibration protocol before reading the holdout labels.

Report acceptance coverage, mean/max normalized error on accepted images, false acceptance on unreadable inputs, review/retake action success, results by gauge and capture condition, baseline comparison, cloud latency and actual cost. Test center/radius calibration errors explicitly. Ask users to complete the capture-and-log task and measure time/errors against manual transcription. Record observations; do not infer adoption or benefit from a plausible use case.
