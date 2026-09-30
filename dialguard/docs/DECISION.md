# Project selection and repository audit

Audit performed September 30, 2026 using the connected GitHub account `akulcanada16-sys`. Seven accessible repositories were returned. Root trees and README files were inspected; relevant image paths in Glossed and the recursive work-samples tree were inspected. This was a targeted reuse audit, not a full security or correctness audit of those repositories.

| Repository | Current purpose and inspected evidence | Reuse judgment |
|---|---|---|
| glossed | Nail inspiration → evidence-backed local business matching; Next.js, Supabase and optional OpenAI image interpretation. Inspected its image interpretation API. | Request limits, provenance, and explicit uncertainty are useful patterns. No OpenCV image engine or AWS runtime found. Repurposing would distort a working product. No code or business data copied. |
| yeti | Windows strategy detection, paper simulation and adaptive trading evidence | Useful trace/evidence design pattern; price bars are not images. No trading code, market data, or broker interfaces copied. |
| projectx-strategy | Causal futures backtesting and reproducibility | Useful seeded-evaluation and failure-disclosure pattern; unrelated workload. No code copied. |
| seb-lab | Python/browser futures research bench | Useful same-core-across-transports pattern; no reusable CV workload found. No code copied. |
| boss-plugin-csv-review | Java CSV quality-review plugin | Different host, language, and input. No code copied. |
| boss-plugins | Plugin/submodule catalogue | Host integration is unnecessary complexity. No plugin code copied. |
| ai-work-samples | Standalone public demonstrations, including RowProof and aerial editing | Suitable isolated home for a first MVP. Its media was not assumed to be competition-ready. No existing sample code or footage copied. |

## Alternatives considered

| Candidate | Main cost/risk | Decision |
|---|---|---|
| Extend Glossed with visual similarity | Catalogue/image rights, AI integration, material AWS migration, and disturbance to an existing product | Too broad for the smallest credible first MVP |
| Turn trading research into screenshot chart analysis | Converting available numeric data to images adds avoidable ambiguity; CV value would be artificial | Reject |
| Generic object detector or video chatbot | Training/weights/licensing, crowded concept, weak evidence-to-action loop | Reject for first MVP |
| Calibrated gauge capture and review | Commodity task, but narrow geometry, no model training, measurable error and rejection behavior | Select DialGuard |

## Scope and scoring judgment

The official rubric weights technical execution 30%, innovation 20%, real-world impact 20%, UX 10%, documentation 10%, and cloud/reproducibility/responsible operation 10%. A narrow tool with truthful evaluation and visible failure handling is feasible within the remaining build period. This is an engineering judgment, not a probability of winning. Gauge reading itself is established; the weakest scoring areas today are innovation and independently demonstrated real-world usefulness.

Target use: low-stakes maintenance documentation of calibrated dials. Proposed benefit: reducing transcription effort while keeping source evidence and refusing some poor captures. No time saving, user adoption, safety benefit, or reliability in the field has yet been measured.

The first version deliberately excludes OCR, automatic scale recognition, gauge localization, perspective rectification, video tracking, LLM explanations, hardware control, model training and COOL. Every addition must justify its complexity with held-out task results.

## Repository decision

The GitHub connector can write branches/files but exposes no new-repository creation tool. `ai-work-samples` is already a collection of self-contained demonstrations, so an isolated `dialguard/` directory on a dedicated branch preserves its purpose. No existing application is changed. The application can move intact into a dedicated `dialguard` repository later. A dedicated repository remains cleaner for final judge navigation; it is not necessary to deliver this first MVP.
