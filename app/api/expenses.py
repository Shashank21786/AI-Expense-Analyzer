from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import (
    TransactionCategoryUpdate,
    TransactionCreate,
    TransactionIngest,
    TransactionResponse,
    TransactionUpdate,
)
from app.services.category_decision_service import decide_category
from app.services.merchant_preference_service import save_merchant_preference
from app.services.merchant_service import normalize_merchant


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
)


@router.post(
    "",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_expense(
    expense_data: TransactionCreate,
    db: Session = Depends(get_db),
):
    transaction = Transaction(
        amount=expense_data.amount,
        merchant=normalize_merchant(expense_data.merchant),
        category=expense_data.category,
        transaction_date=expense_data.transaction_date,
        description=expense_data.description,
        transaction_type=expense_data.transaction_type.value,
        source=expense_data.source,
        confidence=expense_data.confidence,
        status="completed",
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


@router.get(
    "",
    response_model=list[TransactionResponse],
)
def get_expenses(
    db: Session = Depends(get_db),
):
    transactions = (
        db.query(Transaction)
        .order_by(Transaction.transaction_date.desc())
        .all()
    )

    return transactions


@router.get(
    "/pending",
    response_model=list[TransactionResponse],
)
def get_pending_expenses(
    db: Session = Depends(get_db),
):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.status == "pending")
        .order_by(Transaction.transaction_date.desc())
        .all()
    )

    return transactions


@router.post(
    "/ingest",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def ingest_transaction(
    transaction_data: TransactionIngest,
    db: Session = Depends(get_db),
):
    # 1. Check whether this transaction already exists
    if transaction_data.fingerprint:

        existing_transaction = (
            db.query(Transaction)
            .filter(Transaction.fingerprint == transaction_data.fingerprint)
            .first()
        )

        if existing_transaction:

            return existing_transaction

    merchant = normalize_merchant(
        transaction_data.merchant
    )

    decision = decide_category(
        db=db,
        merchant=merchant,
        raw_text=transaction_data.raw_text,
    )

    category = decision.category
    category_source = decision.category_source
    confidence = decision.confidence

    transaction_status = (
        "completed"
        if category
        else "pending"
    )

    transaction = Transaction(
        amount=transaction_data.amount,
        merchant=merchant,
        category=category,
        confidence=confidence,
        fingerprint=transaction_data.fingerprint,
        transaction_date=transaction_data.transaction_date.date(),
        transaction_type=transaction_data.transaction_type.value,
        raw_text=transaction_data.raw_text,
        source_app=transaction_data.source_app,
        source="notification",
        status=transaction_status,
        raw_text=transaction_data.raw_text,
        source_app=transaction_data.source_app,
        category_source=decision.category_source,
        fingerprint=transaction_data.fingerprint,
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


@router.get(
    "/{expense_id}",
    response_model=TransactionResponse,
)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
):
    transaction = db.get(
        Transaction,
        expense_id,
    )

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    return transaction


@router.patch(
    "/{expense_id}",
    response_model=TransactionResponse,
)
def update_expense(
    expense_id: int,
    expense_data: TransactionUpdate,
    db: Session = Depends(get_db),
):
    transaction = db.get(
        Transaction,
        expense_id,
    )

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    if expense_data.amount is not None:
        transaction.amount = expense_data.amount

    if expense_data.merchant is not None:
        transaction.merchant = normalize_merchant(
            expense_data.merchant
        )

    if expense_data.category is not None:
        transaction.category = expense_data.category

    if expense_data.transaction_date is not None:
        transaction.transaction_date = (
            expense_data.transaction_date
        )

    if expense_data.description is not None:
        transaction.description = (
            expense_data.description
        )

    if expense_data.transaction_type is not None:
        transaction.transaction_type = (
            expense_data.transaction_type.value
        )

    if expense_data.source is not None:
        transaction.source = expense_data.source

    if expense_data.confidence is not None:
        transaction.confidence = (
            expense_data.confidence
        )

    db.commit()
    db.refresh(transaction)

    return transaction


@router.patch(
    "/{expense_id}/category",
    response_model=TransactionResponse,
)
def categorize_expense(
    expense_id: int,
    category_data: TransactionCategoryUpdate,
    db: Session = Depends(get_db),
):
    # Find the transaction by ID.
    transaction = db.get(Transaction, expense_id)

    # Return 404 if the transaction does not exist.
    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    # Update the category selected by the user.
    transaction.category = category_data.category

    # The transaction is now completed.
    transaction.status = "completed"

    # Record that the category was selected by the user.
    transaction.category_source = "user"

    # User-selected categories do not need AI confidence.
    transaction.confidence = None

    # Save the merchant/category preference.
    save_merchant_preference(
        db=db,
        merchant=transaction.merchant,
        category=category_data.category,
    )

    # Save the changes.
    db.commit()

    # Refresh the transaction with the latest database values.
    db.refresh(transaction)

    return transaction


@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
):
    transaction = db.get(
        Transaction,
        expense_id,
    )

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    db.delete(transaction)
    db.commit()

    return None
