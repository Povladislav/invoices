from sqlalchemy import select
from sqlalchemy.orm import Session

from models.invoice import Invoice


class InvoiceRepository:
    def __init__(self, session: Session):
        self.session = session

    async def get_invoices(self, skip: int, limit: int):
        # Prepare the query to fetch invoices (without executing it)
        async with self.session.begin():
            invoices_query = select(Invoice.id, Invoice.title, Invoice.discount)
            # Execute the query asynchronously
            invoices_results = await self.session.execute(invoices_query)
            # Get all fetched invoices
            invoices = invoices_results.all()

        return invoices[skip : skip + limit]
