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

## Evaluation

- [x] Baseline deterministic unit tests pass (4/4 observed in CloudShell).
- [x] Expanded authority matrix committed.
- [ ] Rerun expanded suite and record final pass count.
- [x] AWS identity validation passed.
- [x] Bedrock control-plane validation passed.
- [x] Quota-throttle behavior captured without automatic retry.
- [ ] One successful Bedrock model response captured.
- [ ] End-to-end agent flow demonstrated with evidence.

## Cost and safety

- [x] No paid infrastructure provisioned by repository code.
- [x] Inference requires explicit invocation.
- [x] Model fallback is not automatic.
- [x] Financial, contractual, legal, ownership, release/publication actions require human review.
- [x] Governance-bypass requests are blocked.
- [x] Secrets/credentials are not committed.

## Submission assets

- [ ] Final public README reviewed for judges.
- [ ] Architecture diagram finalized.
- [ ] Demo scenario selected.
- [ ] Demo script finalized.
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
