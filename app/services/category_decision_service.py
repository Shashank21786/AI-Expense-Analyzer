from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.services.ai_category_service import (
    categorize_with_ai,
)
from app.services.category_service import (
    get_merchant_category,
)
from app.services.merchant_preference_service import (
    get_merchant_preference,
)


@dataclass
class CategoryDecision:

    category: str | None

    category_source: str | None

    confidence: float | None


def decide_category(
    db: Session,
    merchant: str | None,
    raw_text: str | None,
) -> CategoryDecision:

    # First check hard-coded merchant rules.
    category = get_merchant_category(
        merchant
    )

    if category is not None:

        return CategoryDecision(
            category=category,
            category_source="rule",
            confidence=None,
        )

    # Then check categories learned from the user.
    category = get_merchant_preference(
        db,
        merchant,
    )

    if category is not None:

        return CategoryDecision(
            category=category,
            category_source="user",
            confidence=None,
        )

    # Finally use Gemini AI.
    try:

        ai_result = categorize_with_ai(
            merchant=merchant,
            raw_text=raw_text,
        )

        if (
            ai_result.category is not None
            and ai_result.confidence >= 0.85
        ):

            return CategoryDecision(
                category=ai_result.category,
                category_source="ai",
                confidence=ai_result.confidence,
            )

    except Exception:
        pass

    # Unknown or low-confidence transaction.
    return CategoryDecision(
        category=None,
        category_source=None,
        confidence=None,
    )