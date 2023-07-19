from typing import List
from pydantic import BaseModel


class InvoiceLineSchema(BaseModel):
    title: str
    quantity: int
    price_per_one: float
    subtotal_line: float


class InvoiceOutSchema(BaseModel):
    title: str
    subtotal: float
    total: float
    lines: List[InvoiceLineSchema]

    class Config:
        from_attributes = True
