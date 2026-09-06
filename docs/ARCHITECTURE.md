# DecisionFlow Architecture

## Objective

DecisionFlow is designed to automate routine, reversible operational work while preserving explicit human authority over consequential decisions.

## Control flow

```text
Natural-language task
        |
        v
Strands Agent + Amazon Bedrock
(reasoning, summarization, planning)
        |
        v
Deterministic Decision Gate
        |
        +--> AUTO_EXECUTE
        |      Routine, reversible work
        |      -> execute with available tools
        |      -> record evidence
        |
        +--> HUMAN_REVIEW
        |      Financial / contractual / legal /
        |      ownership / release / publication
        |      -> stop
        |      -> present evidence + risk + exact approval needed
        |
        +--> BLOCK
               Governance bypass / secret exposure /
               audit disabling / guardrail removal
               -> refuse execution
               -> record control outcome
```

## Separation of responsibilities

### Probabilistic layer

The Strands Agent backed by Amazon Bedrock is responsible for tasks that benefit from language-model reasoning:

- interpreting natural-language intent;
- summarizing context;
- decomposing multi-step work;
- deciding which available tool is relevant;
- producing concise human-facing explanations.

### Deterministic layer

The authority boundary is intentionally implemented outside the model in `src/policy.py`.

It returns exactly one of:

- `AUTO_EXECUTE`
- `HUMAN_REVIEW`
- `BLOCK`

The deterministic layer evaluates `BLOCK` rules first, so non-bypassable governance controls take precedence over otherwise reviewable actions.

## Safety properties

1. **No silent approval** — consequential actions require explicit human authorization.
2. **Block precedence** — a bypass instruction cannot be downgraded to human review merely because the same request contains a normal consequential action.
3. **Evidence-first behavior** — completed or escalated actions can be recorded through the evidence tool.
4. **No automatic model fallback** — quota or provider failure does not silently trigger another potentially billable model.
5. **No automatic infrastructure provisioning** — repository code does not create paid AWS infrastructure.
6. **Boundary-safe matching** — policy phrases are matched as words/phrases rather than arbitrary substrings to reduce false positives such as `pay` inside `payload`.

## Validation layers

### Layer 1 — dependency-free policy validation

`python -m scripts.live_validation --region us-east-2`

Checks AWS identity, Bedrock control-plane visibility, and deterministic authority outcomes without Strands model inference.

### Layer 2 — local unit tests

`pytest -q`

Exercises routine, review, block, precedence, normalization, and matching-boundary behavior.

### Layer 3 — controlled model validation

`python -m scripts.one_inference_validation --region us-east-2`

Runs only after explicit authorization. It attaches zero tools and requests one model turn to create end-to-end Strands + Bedrock evidence without agent tool loops.

## Current evidence status

- AWS identity: validated.
- Bedrock control plane: validated in `us-east-2`.
- Deterministic tests: validated through the expanded suite before the latest boundary-hardening change; final rerun is required after that change.
- Bedrock model response: not yet validated successfully because the first authorized attempt was throttled by a daily token quota.

## Judge-facing thesis

The differentiator is not unrestricted autonomy. It is **bounded autonomy**: use AI where interpretation and planning add value, but keep authority and stop conditions deterministic, inspectable, and human-controlled.
