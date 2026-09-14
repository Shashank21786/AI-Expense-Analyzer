from datetime import date,datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field
from pydantic import BaseModel, field_validator


class TransactionType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"


class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    merchant: str = Field(min_length=1, max_length=255)
    category: str = Field(min_length=1, max_length=100)
    transaction_date: date
    description: str | None = Field(default=None, max_length=500)
    transaction_type: TransactionType = TransactionType.EXPENSE


class TransactionResponse(BaseModel):
    id: int
    amount: Decimal
    merchant: str
    category: str | None = None
    category_source: str | None = None
    transaction_date: date
    description: str | None
    transaction_type: TransactionType
    source: str
    confidence: Decimal | None = None
    status: str
    raw_text: str | None
    source_app: str | None
    fingerprint: str | None = None
    model_config = ConfigDict(from_attributes=True)


class TransactionUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0)
    merchant: str | None = Field(default=None, min_length=1, max_length=255)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    transaction_date: date | None = None
    description: str | None = Field(default=None, max_length=500)
    transaction_type: TransactionType | None = None

class TransactionIngest(BaseModel):
    amount: Decimal = Field(gt=0)
    merchant: str | None = None
    transaction_date: datetime
    transaction_type: TransactionType = TransactionType.EXPENSE
    raw_text: str | None = None
    source_app: str | None = None
    fingerprint: str | None = None,


class TransactionCategoryUpdate(BaseModel):
    category: str

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        allowed_categories = {
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

        if value not in allowed_categories:
            raise ValueError("Invalid category")

        return value