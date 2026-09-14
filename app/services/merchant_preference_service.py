from sqlalchemy.orm import Session

from app.models.merchant_preference import (
    MerchantPreference,
)
from app.services.merchant_service import (
    normalize_merchant,
)


def get_merchant_preference(
    db: Session,
    merchant: str | None,
) -> str | None:

    normalized_merchant = normalize_merchant(
        merchant
    )

    if not normalized_merchant:
        return None

    preference = (
        db.query(MerchantPreference)
        .filter(
            MerchantPreference.merchant
            == normalized_merchant
        )
        .first()
    )

    if preference is None:
        return None

    return preference.category


def save_merchant_preference(
    db: Session,
    merchant: str | None,
    category: str,
) -> MerchantPreference:

    normalized_merchant = normalize_merchant(
        merchant
    )

    if not normalized_merchant:
        raise ValueError(
            "Merchant is required"
        )

    preference = (
        db.query(MerchantPreference)
        .filter(
            MerchantPreference.merchant
            == normalized_merchant
        )
        .first()
    )

    if preference is None:

        preference = MerchantPreference(
            merchant=normalized_merchant,
            category=category,
        )

        db.add(preference)

    else:

        preference.category = category

    db.commit()

    db.refresh(preference)

    return preference