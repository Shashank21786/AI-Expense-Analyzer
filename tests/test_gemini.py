from app.services.ai_category_service import (
    build_category_prompt,
    parse_ai_category,
    validate_ai_result,
)


def test_build_category_prompt():
    prompt = build_category_prompt(
        merchant="ABC Lifestyle Store",
        raw_text="₹1250 paid to ABC Lifestyle Store",
    )

    assert "abc lifestyle store" in prompt
    assert "₹1250 paid to ABC Lifestyle Store" in prompt
    assert "Shopping" in prompt


def test_parse_valid_ai_response():
    category, confidence = parse_ai_category(
        """
        {
            "category": "Shopping",
            "confidence": 0.92
        }
        """
    )

    assert category == "Shopping"
    assert confidence == 0.92


def test_parse_invalid_category():
    category, confidence = parse_ai_category(
        """
        {
            "category": "RandomCategory",
            "confidence": 0.90
        }
        """
    )

    assert category is None
    assert confidence == 0.0


def test_parse_invalid_json():
    category, confidence = parse_ai_category(
        "This is not valid JSON"
    )

    assert category is None
    assert confidence == 0.0


def test_parse_markdown_json():
    category, confidence = parse_ai_category(
        """
        ```json
        {
            "category": "Food",
            "confidence": 0.95
        }
        ```
        """
    )

    assert category == "Food"
    assert confidence == 0.95


def test_validate_valid_result():
    result = validate_ai_result(
        category="Transport",
        confidence=0.90,
    )

    assert result.category == "Transport"
    assert result.confidence == 0.90


def test_validate_invalid_result():
    result = validate_ai_result(
        category="Invalid",
        confidence=0.90,
    )

    assert result.category is None
    assert result.confidence == 0.0


def test_validate_confidence_above_one():
    result = validate_ai_result(
        category="Food",
        confidence=1.5,
    )

    assert result.category == "Food"
    assert result.confidence == 1.0


def test_validate_confidence_below_zero():
    result = validate_ai_result(
        category="Food",
        confidence=-0.5,
    )

    assert result.category == "Food"
    assert result.confidence == 0.0