from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone

from strands import Agent
from strands.models import BedrockModel


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

    # No tools are attached. This keeps the validation to a single model turn and avoids
    # agent tool loops that could trigger additional model calls.
    agent = Agent(
        model=model,
        tools=[],
        system_prompt=(
            "You are a concise validation agent. Answer the user's request directly in one sentence. "
            "Do not call tools and do not ask follow-up questions."
        ),
    )

    response = agent(prompt)

    evidence = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "region": args.region,
        "model_id": args.model_id,
        "strands_agent_used": True,
        "bedrock_model_used": True,
        "tools_attached": 0,
        "validation_turns_requested": 1,
        "prompt": prompt,
        "response": str(response),
    }
    print(json.dumps(evidence, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
