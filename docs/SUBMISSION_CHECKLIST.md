# Agents for Humans — Submission Readiness Checklist

## Core product

- [x] Named user and repetitive-work problem defined.
- [x] Strands Agents SDK integrated in the prototype.
- [x] Amazon Bedrock model provider integrated.
- [x] Deterministic authority boundary implemented.
- [x] Human-review and hard-block paths implemented.
- [x] Evidence-recording tool implemented.
- [x] No-inference AWS/Bedrock validator implemented.
- [x] Controlled single-turn inference validator implemented.
- [x] Whole-word / phrase policy matching added to reduce substring false positives.
- [x] No-inference deterministic demo runner implemented.

## Evaluation

- [x] Baseline deterministic unit tests passed (4/4 observed in CloudShell).
- [x] Expanded authority matrix passed (18/18 observed in CloudShell).
- [x] Latest hardened deterministic suite passed (21/21 in 0.42s observed in CloudShell).
- [x] Block-over-review precedence test implemented.
- [x] Policy-boundary regression tests passed.
- [x] AWS identity validation passed.
- [x] Bedrock control-plane validation passed.
- [x] Quota-throttle behavior captured without automatic retry.
- [ ] Capture no-inference policy demo output.
- [ ] One successful Bedrock model response captured.
- [ ] End-to-end agent flow demonstrated with successful model evidence.

## Cost and safety

- [x] No paid infrastructure provisioned by repository code.
- [x] Inference requires explicit invocation.
- [x] Model fallback is not automatic.
- [x] Financial, contractual, legal, ownership, release/publication actions require human review.
- [x] Governance-bypass requests are blocked.
- [x] Secrets/credentials are not committed.

## Submission assets

- [x] Judge-facing README substantially prepared.
- [x] Architecture document created.
- [x] Demo scenario selected.
- [x] Core demo script drafted.
- [ ] Demo video recorded and checked against time limit.
- [ ] Public repository reviewed for proprietary/sensitive material.
- [ ] Submission form completed.
- [ ] Final URLs verified from a signed-out browser.

## Human-required gates

The following are not autonomous actions:

- approving additional potentially billable inference attempts;
- merging the hackathon branch;
- deploying or publishing a public demo;
- recording/approving final public-facing claims;
- submitting the hackathon entry.
