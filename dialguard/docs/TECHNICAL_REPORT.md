# DialGuard technical report — first MVP

## Problem and users

Analog instruments often require a person to read and transcribe a dial. DialGuard explores a small capture workflow: calibrated photo → supported needle estimate → reading or specific request for another capture → review above an operator threshold. Intended users are people documenting low-stakes equipment readings. The problem's frequency and the product's benefit have not been measured with users.

## Implementation

Manual calibration defines normalized hub, dial radius, minimum/maximum, start angle, clockwise angular sweep, unit and optional review threshold. Angles use image coordinates (right 0°, down 90°). Only linear increasing scales are supported. Calibration is an operator assertion, not an automatically verified fact.

OpenCV 5.0.0 runs the actual analysis. `cv2.imdecode` reads PNG/JPEG; `cvtColor` produces grayscale. Laplacian variance and crop mean brightness reject some poor captures. Canny edges and `HoughLinesP` produce a simple independent baseline. The primary detector uses `cv2.remap` to sample radial rays from 24–72% of the calibrated radius, excluding the hub and most tick marks. Each ray receives dark-pixel support across both halves. A weak ray or a competing direction produces a retake request. Otherwise the chosen angle determines the next tool's fine search window; two contrast settings check estimate stability. The accepted angle maps linearly onto the configured scale. Out-of-scale angles are rejected. Threshold crossings request human review; no machinery is controlled.

The source accommodates OpenCV 5's N×4 Hough line output rather than assuming the older N×1×4 binding shape. The version guard prevents accidentally shipping the workload with OpenCV 4.

Ray support/peak margin are diagnostic scores, not probability estimates. Camera roll or faulty scale calibration can yield a convincing but wrong answer. The engine does not recognize instrument identity, read text, rectify perspective or establish that the object is a gauge.

## Architecture and AWS

The transport-independent `analyze` function is used by the local standard-library HTTP server and the AWS Lambda handler. Both serve the same UI and JSON contract. The AWS SAM template provisions an x86_64 Lambda container, Function URL, private S3 bucket and short-lived CloudWatch logs. Lambda hosts substantive CV work. S3 receives only derived evidence and source hash, expiring after seven days.

See [architecture.svg](architecture.svg). AWS deployment has not been performed; no cloud latency, reliability, cost, or COOL acceleration claim is made. Container build and SAM lint also remain pending in a Docker/AWS-enabled environment.

## Evaluation

The first frozen procedural suite uses 128 generated images across clean/noisy readable images and blurred/dark/missing/ambiguous captures. Interactive examples use different fixed readings from evaluation random angles. Per-case source/input hashes, seeds, truth, outputs, error and timings are committed. There is no learning phase; thresholds are development choices, not independent validation. Exact results and the limitations are in `evidence/benchmark.json` and [EVALUATION.md](EVALUATION.md).

The test suite checks angle-to-value behavior, failure decisions, invalid calibration/images, out-of-scale refusal, access codes, Lambda request handling and derived-only S3 writes through a mock. An HTTP smoke exercises the live local endpoint. Browser verification exercises displayed reading, review, retake, upload, evidence download and mobile layout.

Natural-photo evidence currently consists of one exploratory public-domain photo, with no verified numerical ground truth. It was rejected using a manually specified exploratory calibration. It is not a field benchmark or proof of reliable tilt detection.

## Responsible operation and limitations

Use only media you have the rights/consent to process. Raw input/annotated photos are not retained by the application. AWS derived evidence may contain equipment readings/calibration, so avoid sensitive instruments and restrict judge access. The cloud code requires a demo access code, bounds inputs, uses least-privilege S3 writes and short retention. Public GET endpoints and cumulative invocation costs remain risks for a widely shared demo; no production security certification is claimed.

This tool does not diagnose equipment, validate safety, or make maintenance decisions. Users own calibration and confirmation. A wrong reading can be accepted, especially with perspective distortion, wrong hub/scale, shadows, printed text or nonstandard needles. A positive synthetic test is not a safety claim.

## Competition status and next evidence

The project has a complete locally executable first slice and an AWS deployment path. Before submission: deploy and measure on AWS, collect rights-cleared photos from multiple real gauges with independently recorded readings, freeze/tune on distinct development data, evaluate held-out gauges, disclose all failure cases, test with target users, and record the team/demo video. Claims should remain limited to observations actually measured.

AI coding assistance was used to design, implement, test and document this MVP. This report does not claim Akul manually reviewed the source, collected field readings, or submitted the entry.
