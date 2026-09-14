"""add merchant preferences

Revision ID: baf1f34ebd61
Revises: 97b0a3f4c4df
Create Date: 2026-09-13 20:52:12.134743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'baf1f34ebd61'
down_revision: Union[str, Sequence[str], None] = '97b0a3f4c4df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the merchant_preferences table."""

    op.create_table(
        "merchant_preferences",

        # Primary key for each merchant preference.
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),

        # Normalized merchant name.
        sa.Column(
            "merchant",
            sa.String(length=100),
            nullable=False,
        ),

        # Category selected by the user.
        sa.Column(
            "category",
            sa.String(length=100),
            nullable=False,
        ),

        # Primary key constraint.
        sa.PrimaryKeyConstraint("id"),

        # One preference per merchant.
        sa.UniqueConstraint("merchant"),
    )


def downgrade() -> None:
    """Remove the merchant_preferences table."""

    op.drop_table("merchant_preferences")