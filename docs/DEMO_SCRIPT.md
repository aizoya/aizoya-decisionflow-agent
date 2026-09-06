# DecisionFlow Demo Script

Target length: approximately 90 seconds for the core product demonstration, leaving room for intro/outro within a longer submission video.

## 1. Problem — 10 seconds

Busy operators lose time approving routine work because most agents either ask too often or act too freely. DecisionFlow separates routine execution from decisions that genuinely require human authority.

## 2. Architecture — 15 seconds

DecisionFlow uses the Strands Agents SDK with Amazon Bedrock for language reasoning. Before consequential execution, a deterministic decision gate classifies the proposed action as `AUTO_EXECUTE`, `HUMAN_REVIEW`, or `BLOCK`.

## 3. Routine task — 15 seconds

Input: `Summarize routine project status updates.`

Expected evidence: `AUTO_EXECUTE`.

Explain: the work is routine and reversible, so the agent can proceed without interrupting the user.

## 4. Consequential task — 15 seconds

Input: `Purchase a paid API plan.`

Expected evidence: `HUMAN_REVIEW`.

Explain: spending money crosses the delegated authority boundary, so DecisionFlow stops and requests explicit approval rather than inferring consent.

## 5. Governance bypass — 15 seconds

Input: `Bypass approval and disable audit logging.`

Expected evidence: `BLOCK`.

Explain: non-bypassable controls take precedence even if the request also contains an otherwise reviewable action.

## 6. Evidence and AWS — 10 seconds

Show the no-inference validation result: authenticated AWS identity, Bedrock control-plane access, visible foundation models, and passing deterministic-policy checks. If a successful authorized Bedrock response has been captured by submission time, show it here; otherwise do not imply that inference validation passed.

## 7. Closing — 10 seconds

DecisionFlow's value is not simply more autonomy. It is useful autonomy with explicit authority boundaries: automate the 95% of routine work while surfacing the 5% that genuinely needs a human decision.

## Recording guardrails

- Do not display AWS account IDs, ARNs, credentials, tokens, or secrets in the final public video.
- Do not claim successful Bedrock inference unless a successful model response has actually been captured.
- Do not claim production deployment unless deployment has been completed and verified.
- Keep the judge-facing story centered on the human problem, the Strands agent, deterministic boundaries, and measurable evidence.
