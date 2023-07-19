from sqlalchemy import select

from models.invoiceline import InvoiceLine
from repository import InvoiceRepository


class InvoiceService:
    def __init__(self, invoice_repository: InvoiceRepository):
        self.invoice_repository = invoice_repository

    async def get_invoices_with_totals(
        self, skip: int, limit: int, total_sum_gte: float, total_sum_lte: float
    ):
        invoices = await self.invoice_repository.get_invoices(skip, limit)

        invoices_list = []
        invoices_count = 0
        invoices_total = 0

        for invoice in invoices:
            # Extract invoice details
            invoice_id, invoice_title, invoice_discount = invoice

            # Prepare the query to fetch lines for the current invoice (without executing it)
            lines_query = select(
                InvoiceLine.title,
                InvoiceLine.quantity,
                InvoiceLine.price_per_one,
                (InvoiceLine.quantity * InvoiceLine.price_per_one).label(
                    "subtotal_line"
                ),
            ).where(InvoiceLine.id == invoice_id)

            # Execute the query asynchronously
            lines_results = await self.invoice_repository.session.execute(lines_query)
            # Get all fetched lines for the current invoice
            lines = lines_results.all()

            # Calculate subtotal and total for the current invoice
            subtotal = sum(line["subtotal_line"] for line in lines)
            total = subtotal - (subtotal * invoice_discount)

            # Filter invoices by total_sum_gte and total_sum_lte (if provided)
            if total_sum_gte is not None and total < total_sum_gte:
                continue
            if total_sum_lte is not None and total > total_sum_lte:
                continue

            # Append the processed invoice data to the list
            invoices_list.append(
                {
                    "title": invoice_title,
                    "subtotal": str(subtotal),
                    "total": str(total),
                    "lines": lines,
                }
            )

            # Update invoices_count and invoices_total
            invoices_count += 1
            invoices_total += total

        # Return the final result in the required format
        return {
            "invoices": invoices_list,
            "invoices_count": invoices_count,
            "invoices_total": str(invoices_total),
        }
