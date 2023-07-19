from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base
from models.base import BaseModel


class InvoiceLine(Base, BaseModel):
    __tablename__ = "lines"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price_per_one = Mapped[Decimal] = mapped_column()
