from app.services.merchant_service import normalize_merchant


MERCHANT_CATEGORIES = {
    "swiggy": "Food",
    "zomato": "Food",
    "uber": "Transport",
    "ola": "Transport",
    "netflix": "Entertainment",
    "amazon": "Shopping",
    "flipkart": "Shopping",
    "airtel": "Bills",
    "jio": "Bills",
}


def get_merchant_category(
    merchant: str | None,
) -> str | None:

    normalized_merchant = normalize_merchant(
        merchant
    )

    if not normalized_merchant:
        return None

    return MERCHANT_CATEGORIES.get(
        normalized_merchant
    )