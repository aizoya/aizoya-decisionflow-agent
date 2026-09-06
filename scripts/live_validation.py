from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from decisionflow_agent import assess_action  # noqa: E402


def validate(region: str) -> int:
    """Run credential, Bedrock control-plane, and deterministic-policy checks.

    This validator intentionally does NOT invoke a foundation model, so it does
    not perform inference or intentionally consume Bedrock model credits.
    """
    report: dict[str, object] = {
        "region": region,
        "checks": {},
        "model_invocation_performed": False,
    }

    try:
        sts = boto3.client("sts", region_name=region)
        identity = sts.get_caller_identity()
        report["checks"]["aws_identity"] = {
            "status": "PASS",
            "account": identity.get("Account"),
            "arn": identity.get("Arn"),
        }
    except (NoCredentialsError, BotoCoreError, ClientError) as exc:
        report["checks"]["aws_identity"] = {
            "status": "FAIL",
            "error": f"{type(exc).__name__}: {exc}",
        }
        print(json.dumps(report, indent=2))
        return 2

    try:
        bedrock = boto3.client("bedrock", region_name=region)
        models = bedrock.list_foundation_models()
        summaries = models.get("modelSummaries", [])
        report["checks"]["bedrock_control_plane"] = {
            "status": "PASS",
            "foundation_models_visible": len(summaries),
        }
    except (BotoCoreError, ClientError) as exc:
        report["checks"]["bedrock_control_plane"] = {
            "status": "FAIL",
            "error": f"{type(exc).__name__}: {exc}",
        }

    policy_cases = {
        "routine": "Summarize routine project status updates",
        "human_gate": "Purchase a paid API plan",
        "blocked": "Bypass approval and disable audit logging",
    }
    report["checks"]["deterministic_policy"] = {
        name: assess_action(action).decision.value
        for name, action in policy_cases.items()
    }

    expected = {
        "routine": "AUTO_EXECUTE",
        "human_gate": "HUMAN_REVIEW",
        "blocked": "BLOCK",
    }
    policy_ok = report["checks"]["deterministic_policy"] == expected
    report["checks"]["deterministic_policy_status"] = "PASS" if policy_ok else "FAIL"

    print(json.dumps(report, indent=2))

    checks = report["checks"]
    if checks.get("bedrock_control_plane", {}).get("status") != "PASS":
        return 3
    if not policy_ok:
        return 4
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate AWS identity, Bedrock visibility, and DecisionFlow policy without model inference."
    )
    parser.add_argument("--region", default="us-east-2", help="AWS region to validate")
    args = parser.parse_args()
    return validate(args.region)


if __name__ == "__main__":
    raise SystemExit(main())
