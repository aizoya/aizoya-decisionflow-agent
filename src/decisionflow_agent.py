from __future__ import annotations

import json
import os
from dataclasses import asdict
from typing import Any

from strands import Agent, tool
from strands.models import BedrockModel

from policy import ActionAssessment, Decision, assess_action


@tool
def decision_gate(action: str) -> str:
    """Classify a proposed action as AUTO_EXECUTE, HUMAN_REVIEW, or BLOCK before execution."""
    assessment = assess_action(action)
    return json.dumps(asdict(assessment), default=str)


@tool
def record_evidence(action: str, outcome: str) -> str:
    """Create a compact audit/evidence record for a completed or escalated action."""
    return json.dumps(
        {
            "action": action,
            "outcome": outcome,
            "evidence_status": "RECORDED",
        }
    )


def build_agent() -> Agent:
    model_id = os.getenv("BEDROCK_MODEL_ID", "global.anthropic.claude-sonnet-4-6")
    region = os.getenv("AWS_REGION", "us-east-2")

    model = BedrockModel(
        model_id=model_id,
        region_name=region,
        temperature=0.1,
    )

    system_prompt = """
You are AIZOYA DecisionFlow, an autonomous executive action agent.

Goal: remove repetitive routine work while surfacing only genuine human decisions.

Operating contract:
1. Before proposing execution, call decision_gate with the exact action.
2. AUTO_EXECUTE: proceed with routine, reversible work using available tools.
3. HUMAN_REVIEW: stop and present the decision, evidence, risk, and exact approval needed.
4. BLOCK: do not execute; explain which control prevented the action.
5. Never infer approval from silence.
6. Record evidence for completed actions and escalations.
7. Prefer deterministic rules for authority boundaries; use the model for reasoning, summarization, and planning.
""".strip()

    return Agent(
        model=model,
        tools=[decision_gate, record_evidence],
        system_prompt=system_prompt,
    )


def run(prompt: str) -> Any:
    return build_agent()(prompt)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run AIZOYA DecisionFlow")
    parser.add_argument("prompt", help="Task or request for the agent")
    args = parser.parse_args()
    print(run(args.prompt))
