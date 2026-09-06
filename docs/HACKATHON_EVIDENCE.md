# Hackathon Evidence Record

## Purpose

This document records reproducible evidence for the AIZOYA DecisionFlow Agent without treating unverified claims as completed validation.

## Architecture claim

DecisionFlow uses the Strands Agents SDK with Amazon Bedrock for natural-language reasoning while enforcing deterministic authority boundaries before consequential execution.

## Validation matrix

| Evidence | Result | Notes |
|---|---|---|
| AWS identity | PASS | AWS CloudShell authenticated successfully. |
| Amazon Bedrock control plane | PASS | `list_foundation_models` succeeded in `us-east-2`; 91 models were visible during validation. |
| Routine-action policy | PASS | Expected `AUTO_EXECUTE`. |
| Human-gated purchase policy | PASS | Expected `HUMAN_REVIEW`. |
| Governance-bypass policy | PASS | Expected `BLOCK`. |
| Python dependency installation | PASS | Project and Strands dependencies installed in isolated `.venv`. |
| Unit tests | PASS | Initial suite: 4 tests passed. Expanded deterministic policy matrix added afterward and requires local rerun. |
| Controlled Strands + Bedrock inference | BLOCKED BY QUOTA | The authorized attempt reached Bedrock `ConverseStream` but returned `ThrottlingException: Too many tokens per day`. No successful model response was received. |

## Cost-control evidence

- No infrastructure provisioning is performed by repository code.
- The no-inference validator performs AWS identity, Bedrock control-plane, and deterministic-policy checks only.
- The controlled inference validator attaches zero tools to prevent an agent tool loop.
- On a Strands `ModelThrottledException`, the validator exits and instructs the operator not to retry automatically.
- Model switching requires a fresh explicit authorization because it can create another billable inference.

## Human-control evidence

DecisionFlow recognizes three authority states:

1. `AUTO_EXECUTE` — routine, reversible work inside the delegated boundary.
2. `HUMAN_REVIEW` — financial, contractual, legal, ownership, publication/release, and other consequential decisions requiring explicit approval.
3. `BLOCK` — attempts to bypass approval, auditing, secrets protection, or other non-bypassable controls.

`BLOCK` takes precedence over `HUMAN_REVIEW` when a request contains both a consequential action and a governance-bypass instruction.

## Evidence still required before final submission

- Rerun the expanded unit-test matrix and record the pass count.
- Obtain one successful Strands + Bedrock inference after quota reset or explicitly approved fallback-model use.
- Capture the successful inference output as submission evidence.
- Validate the complete demo path and create the final demo script/video.
- Human review before merging, publishing, deploying, or submitting.
