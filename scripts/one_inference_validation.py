from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone

from strands import Agent
from strands.models import BedrockModel
from strands.types.exceptions import ModelThrottledException


def evidence_base(region: str, model_id: str) -> dict[str, object]:
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "region": region,
        "model_id": model_id,
        "strands_agent_used": True,
        "bedrock_model_used": True,
        "tools_attached": 0,
        "validation_turns_requested": 1,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run exactly one controlled Strands/Bedrock model turn for hackathon evidence."
    )
    parser.add_argument("--region", default="us-east-2")
    parser.add_argument(
        "--model-id",
        default=os.getenv("BEDROCK_MODEL_ID", "global.anthropic.claude-sonnet-4-6"),
    )
    args = parser.parse_args()

    prompt = (
        "In one sentence, explain the DecisionFlow principle: routine reversible work can be automated, "
        "but financial, contractual, legal, ownership, release, publication, and governance-bypass actions "
        "must require explicit human review or be blocked."
    )

    model = BedrockModel(
        model_id=args.model_id,
        region_name=args.region,
        temperature=0.0,
    )

    # No tools are attached. This keeps the validation to a single requested model turn and avoids
    # agent tool loops that could trigger additional model calls.
    agent = Agent(
        model=model,
        tools=[],
        system_prompt=(
            "You are a concise validation agent. Answer the user's request directly in one sentence. "
            "Do not call tools and do not ask follow-up questions."
        ),
    )

    evidence = evidence_base(args.region, args.model_id)
    evidence["prompt"] = prompt

    try:
        response = agent(prompt)
    except ModelThrottledException as exc:
        evidence.update(
            {
                "status": "THROTTLED",
                "model_response_received": False,
                "error_type": type(exc).__name__,
                "error": str(exc),
                "next_action": (
                    "Do not retry automatically. Wait for quota reset or obtain explicit approval "
                    "to validate with a different Bedrock model."
                ),
            }
        )
        print(json.dumps(evidence, indent=2))
        return 5

    evidence.update(
        {
            "status": "PASS",
            "model_response_received": True,
            "response": str(response),
        }
    )
    print(json.dumps(evidence, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
