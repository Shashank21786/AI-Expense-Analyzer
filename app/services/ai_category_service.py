from dataclasses import dataclass
from typing import Literal

from google import genai

from app.core.config import settings

from app.services.merchant_service import normalize_merchant


# Categories supported by our expense analyzer.
Category = Literal[
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Entertainment",
    "Health",
    "Travel",
    "Education",
    "Other",
]


# Keep a normal set as well so we can validate
# category values returned by AI.
ALLOWED_CATEGORIES = {
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Entertainment",
    "Health",
    "Travel",
    "Education",
    "Other",
}


@dataclass
class AICategoryResult:
    # Category predicted by Gemini.
    category: str | None

    # Confidence score between 0 and 1.
    confidence: float


def build_category_prompt(
    merchant: str | None,
    raw_text: str | None,
) -> str:
    # Normalize the merchant before sending it to Gemini.
    normalized_merchant = normalize_merchant(
        merchant
    )

    # Use an empty string when notification text is missing.
    notification_text = raw_text or ""

    return f"""
You are a transaction categorization system.

Categorize the transaction into exactly one of these categories:

Food
Transport
Shopping
Bills
Entertainment
Health
Travel
Education
Other

Rules:

- Food: restaurants, food delivery, groceries and cafes.
- Transport: taxis, ride sharing, fuel and public transport.
- Shopping: online shopping, clothing, electronics and general retail.
- Bills: mobile, internet, electricity, subscriptions and utilities.
- Entertainment: movies, games, streaming and recreational entertainment.
- Health: hospitals, pharmacies, doctors and medical services.
- Travel: flights, hotels, travel bookings and tourism.
- Education: courses, books for study and educational services.
- Other: use when the transaction cannot reasonably be classified.

Merchant:
{normalized_merchant or "Unknown"}

Notification:
{notification_text}

Return ONLY JSON in this exact format:

{{
    "category": "Shopping",
    "confidence": 0.92
}}

The category must be one of the allowed categories.
The confidence must be a number between 0 and 1.
""".strip()


def parse_ai_category(
    ai_response: str,
) -> tuple[str | None, float]:
    # Remove unnecessary whitespace.
    response_text = ai_response.strip()

    # Gemini can sometimes return JSON inside
    # a Markdown code block.
    if response_text.startswith("```"):
        lines = response_text.splitlines()

        # Remove the first line such as ```json.
        if lines:
            lines = lines[1:]

        # Remove the closing ```
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        response_text = "\n".join(lines).strip()

    # Import json only when this function is called.
    import json

    try:
        # Convert Gemini's JSON text into a Python dictionary.
        response_data = json.loads(
            response_text
        )
    except json.JSONDecodeError:
        return None, 0.0

    # Get the category from Gemini's response.
    category = response_data.get("category")

    # Get the confidence from Gemini's response.
    confidence = response_data.get("confidence")

    # Make sure Gemini returned a supported category.
    if category not in ALLOWED_CATEGORIES:
        return None, 0.0

    # Convert confidence into a float.
    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        return None, 0.0

    # Keep confidence between 0 and 1.
    confidence = max(
        0.0,
        min(confidence, 1.0),
    )

    return category, confidence


def validate_ai_result(
    category: str | None,
    confidence: float,
) -> AICategoryResult:
    # Reject categories that are not supported.
    if category not in ALLOWED_CATEGORIES:
        return AICategoryResult(
            category=None,
            confidence=0.0,
        )

    # Keep confidence within the valid range.
    confidence = max(
        0.0,
        min(confidence, 1.0),
    )

    return AICategoryResult(
        category=category,
        confidence=confidence,
    )


def categorize_with_ai(
    merchant: str | None,
    raw_text: str | None,
) -> AICategoryResult:
    # Create the Gemini client only when an AI
    # categorization is actually required.
    client = genai.Client(api_key=settings.gemini_api_key)

    # Build the prompt using the reusable method.
    prompt = build_category_prompt(
        merchant,
        raw_text,
    )

    # Ask Gemini for the category.
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    # Gemini should return text containing JSON.
    if not response.text:
        return AICategoryResult(
            category=None,
            confidence=0.0,
        )

    # Parse Gemini's response.
    category, confidence = parse_ai_category(
        response.text
    )

    # Validate and return the final result.
    return validate_ai_result(
        category,
        confidence,
    )