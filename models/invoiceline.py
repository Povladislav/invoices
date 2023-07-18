from sqlalchemy import DECIMAL, Column, Integer, String

from database.database import Base


class InvoiceLine(Base):
    __tablename__ = "lines"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_one = Column(DECIMAL)
