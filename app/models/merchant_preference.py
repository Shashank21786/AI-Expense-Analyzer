from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class MerchantPreference(Base):

    __tablename__ = "merchant_preferences"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    merchant: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )