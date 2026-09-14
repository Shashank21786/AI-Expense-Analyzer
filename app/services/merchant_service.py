import re


def normalize_merchant(
    merchant: str | None,
) -> str | None:

    if not merchant:
        return None

    merchant = merchant.strip().lower()

    merchant = re.sub(
        r"[^a-z0-9\s]",
        " ",
        merchant,
    )

    merchant = re.sub(
        r"\s+",
        " ",
        merchant,
    )

    return merchant.strip()