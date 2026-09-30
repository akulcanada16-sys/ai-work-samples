# Deploy the meaningful AWS component

**Status: prepared and handler-tested locally; not deployed on AWS.** No AWS credentials/account access was available in the execution environment. The Docker image has not been built here because Docker is unavailable. SAM/CloudFormation validation and cloud smoke testing must run in the actual deployment environment.

AWS is the computation host, not a decorative storage attachment: Lambda runs image decoding, Laplacian quality checks, Canny/Hough baseline, polar remapping, contrast verification, decisions and annotation. S3 stores derived evidence; CloudWatch stores operational metadata. UI and API share one Function URL.

## Prerequisites

- An AWS account/region with Lambda container images, ECR, S3 and Function URLs available; deployment identity with appropriate CloudFormation/IAM permissions.
- AWS CLI authenticated locally, AWS SAM CLI, and Docker (x86_64 build).
- A deliberate account budget/credit plan. No compute grant is assumed. Credits or Free Tier eligibility do not guarantee zero cost.

Authenticate with your existing local AWS SSO/profile. Do not put access keys in this repository or paste credentials into chat. Confirm the target with `aws sts get-caller-identity` in your own terminal.

## Build and deploy

From the self-contained `dialguard` directory:

```sh
sam validate --lint
sam build
sam deploy --guided --resolve-image-repos
```

Use a stack name such as `dialguard-mvp` and choose the account's intended region. Enter a **new, unique demo access code of at least 24 letters/digits/underscore/hyphen** when asked for `DemoToken`. `NoEcho` protects CloudFormation parameter displays. Decline saving deployment parameters to `samconfig.toml`; avoid retaining this access code in configuration or shell history. Allow SAM's required IAM resource creation after reviewing the stack. SAM will provision an ECR repository for the image.

The `DemoUrl` output serves the interface. Share the URL and demo access code with judges through their private access instructions, never in public source. `GET /health` exposes only version and execution mode. Enter the access code in the interface before inspecting an image.

Set `DIALGUARD_TOKEN` in your current terminal using an appropriate secret prompt, then run:

```sh
python scripts/smoke_http.py https://YOUR_FUNCTION_URL/
```

Successful results must say `mode: aws` and OpenCV `5.0.0`. Capture the stack outputs (no token), deployed image digest, AWS region/architecture/memory, health response, an inspection response, CloudWatch invocation evidence, and a corresponding S3 record. Then measure cold/warm latency and cost using the actual service configuration. Local timing does not substitute for this evidence.

## Controls and limitations

- Inspection requests require the demo code; GET pages/samples are public. Use HTTPS Function URLs. Rotate the code if exposed.
- 1.5 MiB PNG/JPEG input and 4 MP decoded-pixel limits; request body capped; Lambda timeout 20 seconds, memory 1024 MB.
- Two reserved concurrent invocations; this constrains bursts, not cumulative spend. Some accounts may need a concurrency quota increase; do not remove the limit silently.
- S3 public access blocked, server-side encryption, PutObject restricted to `inspections/*`, seven-day lifecycle. No raw image or annotated image is stored; reading/calibration/hash/trace are derived data and may still be sensitive.
- Logs omit images and access codes and expire after seven days. No automatic actuator action or autonomous maintenance instruction.
- Static demo code is a small-demo access control, not production identity management. No hard daily quota, per-user authorization, or DDoS protection is claimed. Repeated unauthenticated GET/POST requests can still consume Lambda resources.
- Add an AWS budget alert before broader sharing. Budget alerts are not a hard spending cutoff.

## Remove resources after judging

```sh
sam delete --stack-name dialguard-mvp
```

The evidence bucket is retained to prevent accidental evidence deletion. Inspect/export wanted records, empty and delete that bucket deliberately, and verify ECR image/repository cleanup. Check billing to ensure no remaining resources. Do not delete a shared account resource by name alone.

Primary AWS references: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html and https://docs.aws.amazon.com/lambda/latest/dg/images-create.html
