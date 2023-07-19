from decimal import Decimal

from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base
from models.base import BaseModel


class Invoice(BaseModel):
    __tablename__ = "invoices"
    id: Mapped[int] = mapped_column(ForeignKey("base_model.id"), primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    discount: Mapped[Decimal] = mapped_column(DECIMAL(precision=5, scale=2))
    __mapper_args__ = {
        "polymorphic_identity": "invoices",
        "inherit_condition": id == BaseModel.id
    }
