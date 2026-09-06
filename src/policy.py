from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Decision(str, Enum):
    AUTO_EXECUTE = "AUTO_EXECUTE"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class ActionAssessment:
    action: str
    decision: Decision
    reason: str
    risk_score: int


HUMAN_GATE_TERMS = {
    "purchase",
    "pay",
    "contract",
    "sign",
    "legal",
    "release",
    "publish",
    "delete production",
    "change owner",
    "financial transfer",
}

BLOCK_TERMS = {
    "expose secret",
    "disable audit",
    "bypass approval",
    "remove guardrail",
}


def assess_action(action: str) -> ActionAssessment:
    """Deterministically classify an action before any agentic execution.

    This module intentionally has no Strands or Bedrock dependency so policy
    checks can run in a minimal AWS CloudShell environment before SDK install.
    """
    normalized = " ".join(action.lower().split())

    if any(term in normalized for term in BLOCK_TERMS):
        return ActionAssessment(
            action=action,
            decision=Decision.BLOCK,
            reason="Action conflicts with a non-bypassable safety or governance control.",
            risk_score=100,
        )

    if any(term in normalized for term in HUMAN_GATE_TERMS):
        return ActionAssessment(
            action=action,
            decision=Decision.HUMAN_REVIEW,
            reason="Action requires explicit human judgment or approval.",
            risk_score=80,
        )

    return ActionAssessment(
        action=action,
        decision=Decision.AUTO_EXECUTE,
        reason="Action is routine and falls within the autonomous execution boundary.",
        risk_score=20,
    )
