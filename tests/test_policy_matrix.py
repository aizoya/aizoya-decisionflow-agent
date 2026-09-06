import pytest

from policy import Decision, assess_action


@pytest.mark.parametrize(
    ("action", "expected"),
    [
        ("Summarize routine project updates", Decision.AUTO_EXECUTE),
        ("Draft an internal reversible checklist", Decision.AUTO_EXECUTE),
        ("Organize notes from today's meeting", Decision.AUTO_EXECUTE),
        ("Purchase a paid API plan", Decision.HUMAN_REVIEW),
        ("Pay the vendor invoice", Decision.HUMAN_REVIEW),
        ("Sign the vendor contract", Decision.HUMAN_REVIEW),
        ("Publish the release externally", Decision.HUMAN_REVIEW),
        ("Change owner of the production account", Decision.HUMAN_REVIEW),
        ("Make a financial transfer", Decision.HUMAN_REVIEW),
        ("Expose secret credentials", Decision.BLOCK),
        ("Disable audit logging", Decision.BLOCK),
        ("Bypass approval and continue", Decision.BLOCK),
        ("Remove guardrail protections", Decision.BLOCK),
    ],
)
def test_authority_matrix(action, expected):
    assert assess_action(action).decision is expected


def test_block_precedence_over_human_gate():
    assessment = assess_action("Purchase the plan and bypass approval")
    assert assessment.decision is Decision.BLOCK
    assert assessment.risk_score == 100
