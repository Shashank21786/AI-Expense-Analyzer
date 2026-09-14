from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.transaction import (
    TransactionCreate,
    TransactionType,
)


def test_valid_transaction():
    transaction = TransactionCreate(
        amount=Decimal("450.00"),
        merchant="Swiggy",
        category="Food",
        transaction_date=date(2026, 8, 23),
        description="Food order",
    )

    assert transaction.amount == Decimal("450.00")
    assert transaction.merchant == "Swiggy"
    assert transaction.category == "Food"
    assert transaction.transaction_type == TransactionType.EXPENSE


def test_negative_amount_is_rejected():
    with pytest.raises(ValidationError):
        TransactionCreate(
            amount=Decimal("-100"),
            merchant="Swiggy",
            category="Food",
            transaction_date=date(2026, 8, 23),
        )


def test_empty_merchant_is_rejected():
    with pytest.raises(ValidationError):
        TransactionCreate(
            amount=Decimal("100"),
            merchant="",
            category="Food",
            transaction_date=date(2026, 8, 23),
        )