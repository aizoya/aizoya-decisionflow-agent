from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from policy import assess_action  # noqa: E402


SCENARIOS = [
    "Summarize routine project status updates",
    "Purchase a paid API plan",
    "Bypass approval and disable audit logging",
]


def main() -> int:
    results = []
    for action in SCENARIOS:
        assessment = assess_action(action)
        results.append(asdict(assessment))

    print(
        json.dumps(
            {
                "demo_type": "deterministic_policy_only",
                "bedrock_inference_performed": False,
                "results": results,
            },
            indent=2,
            default=str,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
