from app.services.category_decision_service import decide_category


def test_rule_category():
    decision = decide_category(
        db=None,
        merchant="swiggy",
        raw_text="₹450 paid to SWIGGY",
    )
    print(decision)
    assert decision.category == "Food"
    assert decision.category_source == "rule"
    assert decision.confidence is None