from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DECIMAL
from database.database import Base
from models.base import BaseModel


class InvoiceLine(BaseModel):
    __tablename__ = "lines"
    id: Mapped[int] = mapped_column(ForeignKey("base_model.id"), primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price_per_one: Mapped[Decimal] = mapped_column()
    __mapper_args__ = {
        "polymorphic_identity": "lines",
        "inherit_condition": id == BaseModel.id
    }
