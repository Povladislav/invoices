from sqlalchemy import select
from sqlalchemy.orm import Session

from models.invoice import Invoice
from schemas import InvoiceOutSchema


class InvoiceRepository:
    def __init__(self, session: Session):
        self.session = session

    async def get_invoices(self):
        async with self.session.begin():
            invoices_query = select(Invoice.id, Invoice.title, Invoice.discount)
            invoices_results = await self.session.execute(invoices_query)
            invoices = invoices_results.all()

        return [Invoice(id=invoice.id, title=invoice.title, discount=invoice.discount) async for invoice in invoices]
