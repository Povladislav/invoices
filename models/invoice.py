from sqlalchemy import DECIMAL, Column, Integer, String

from database.database import Base


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    discount = Column(DECIMAL(precision=3, scale=2))
