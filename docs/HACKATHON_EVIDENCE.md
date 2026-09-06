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
| Hardened deterministic unit tests | PASS | Latest policy-boundary-hardened suite: **21 tests passed in 0.42s** in AWS CloudShell. |
| Controlled Strands + Bedrock inference | BLOCKED BY QUOTA | The authorized attempt reached Bedrock `ConverseStream` but returned `ThrottlingException: Too many tokens per day`. No successful model response was received. |

## Cost-control evidence

- No infrastructure provisioning is performed by repository code.
- The no-inference validator performs AWS identity, Bedrock control-plane, and deterministic-policy checks only.
- `python -m scripts.policy_demo` demonstrates the three core authority outcomes without model inference.
- The controlled inference validator attaches zero tools to prevent an agent tool loop.
- On a Strands `ModelThrottledException`, the validator exits and instructs the operator not to retry automatically.
- Model switching requires a fresh explicit authorization because it can create another billable inference.

## Human-control evidence

DecisionFlow recognizes three authority states:

1. `AUTO_EXECUTE` — routine, reversible work inside the delegated boundary.
2. `HUMAN_REVIEW` — financial, contractual, legal, ownership, publication/release, and other consequential decisions requiring explicit approval.
3. `BLOCK` — attempts to bypass approval, auditing, secrets protection, or other non-bypassable controls.

`BLOCK` takes precedence over `HUMAN_REVIEW` when a request contains both a consequential action and a governance-bypass instruction.

The policy matcher evaluates whole words and phrases rather than arbitrary substrings. This prevents a short authority term such as `pay` from accidentally matching a routine term such as `payload`.

## Evidence still required before final submission

- Obtain one successful Strands + Bedrock inference after quota reset or explicitly approved fallback-model use.
- Capture the successful inference output as submission evidence.
- Run and capture the no-inference deterministic demo runner output.
- Validate the complete demo path and record the final demo video.
- Human review before merging, publishing, deploying, or submitting.
