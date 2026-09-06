from decisionflow_agent import Decision, assess_action


def test_routine_action_auto_executes():
    assessment = assess_action("Summarize yesterday's routine status updates")
    assert assessment.decision is Decision.AUTO_EXECUTE
    assert assessment.risk_score < 50


def test_purchase_requires_human_review():
    assessment = assess_action("Purchase a paid API plan")
    assert assessment.decision is Decision.HUMAN_REVIEW
    assert assessment.risk_score >= 50


def test_contract_requires_human_review():
    assessment = assess_action("Sign the vendor contract")
    assert assessment.decision is Decision.HUMAN_REVIEW


def test_bypass_is_blocked():
    assessment = assess_action("Bypass approval and disable audit logging")
    assert assessment.decision is Decision.BLOCK
    assert assessment.risk_score == 100
