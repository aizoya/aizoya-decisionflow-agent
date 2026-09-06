# AIZOYA DecisionFlow Agent

Autonomous executive action agent built with the **Strands Agents SDK** and **Amazon Bedrock**. It handles routine work automatically, uses deterministic authority boundaries, and escalates only decisions that require human judgment.

## Hackathon thesis

People lose time repeatedly deciding whether small operational tasks are safe to execute. DecisionFlow separates **routine execution** from **human authority** so the agent can work in the background without turning every step into another notification.

### Named user

A founder, operator, or busy professional managing recurring administrative work across projects.

### End-to-end flow

```text
TASK
  -> MODEL REASONS ABOUT INTENT
  -> DETERMINISTIC DECISION GATE
      -> AUTO_EXECUTE -> perform routine/reversible work -> record evidence
      -> HUMAN_REVIEW -> present decision + evidence + risk + exact approval
      -> BLOCK -> refuse non-bypassable governance violation
```

## Why AI is necessary

The model interprets natural-language tasks, summarizes context, plans multi-step work, and decides which available tool to call. The authority boundary itself is deterministic so model creativity cannot silently expand permissions.

## Human-control contract

DecisionFlow never infers approval from silence. Financial, contractual, legal, ownership, release, publication, and other high-authority actions are escalated for explicit review. Attempts to bypass approval or auditing are blocked.

## Current prototype

- Strands `Agent`
- Amazon Bedrock model provider
- `decision_gate` Strands tool
- `record_evidence` Strands tool
- deterministic `AUTO_EXECUTE | HUMAN_REVIEW | BLOCK` policy
- unit tests for routine, purchase, contract, and bypass scenarios
- expanded deterministic authority evaluation matrix
- no-inference AWS/Bedrock control-plane validator
- controlled single-turn Strands/Bedrock inference validator
- structured throttle handling with no automatic fallback or retry

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
export AWS_REGION=us-east-2
# Optional: override the default Bedrock model
export BEDROCK_MODEL_ID=global.anthropic.claude-sonnet-4-6
pytest
python src/decisionflow_agent.py "Summarize today's routine project updates"
```

AWS credentials should be provided through the normal AWS credential chain. Do not commit credentials or secrets.

## Validation

No-inference validation:

```bash
python -m scripts.live_validation --region us-east-2
```

Controlled one-turn Strands + Bedrock validation (run only after explicit authorization to incur the model inference):

```bash
python -m scripts.one_inference_validation --region us-east-2
```

The controlled inference validator intentionally attaches no tools so the validation remains one requested model turn and cannot enter an agent tool loop. If Bedrock returns a quota throttle, the script records `THROTTLED` evidence and exits without automatic retry or model switching.

## Evaluation scenarios

| Scenario | Expected decision |
|---|---|
| Summarize routine status updates | `AUTO_EXECUTE` |
| Draft a reversible internal checklist | `AUTO_EXECUTE` |
| Purchase a paid API plan | `HUMAN_REVIEW` |
| Sign a vendor contract | `HUMAN_REVIEW` |
| Publish/release externally | `HUMAN_REVIEW` |
| Bypass approval or disable audit controls | `BLOCK` |

## Evidence and readiness

- [Hackathon evidence record](docs/HACKATHON_EVIDENCE.md)
- [Submission readiness checklist](docs/SUBMISSION_CHECKLIST.md)

Observed validation to date includes successful AWS identity and Bedrock control-plane access, deterministic-policy checks, dependency installation, and a 4/4 baseline unit-test pass. The first authorized model invocation reached Bedrock `ConverseStream` but was rejected by a daily token quota, so a successful model response is **not** claimed yet.

## Cost-control posture

The prototype is intentionally lightweight. No infrastructure is provisioned by this repository. Bedrock inference occurs only when explicitly invoked. AWS billing and promotional-credit usage should be monitored separately.

## Status

Prototype core is under active hackathon development. No production deployment or release is implied by this branch.
