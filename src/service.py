from repository import InvoiceRepository


class InvoiceService:
    def __init__(self, invoice_repository: InvoiceRepository):
        self.invoice_repository = invoice_repository

    async def get_invoices_with_totals(
            self, skip: int, limit: int, total_sum_gte: float, total_sum_lte: float
    ) -> dict:
        invoices = await self.invoice_repository.get_invoices(skip, limit)

        invoices_list = []
        invoices_count = 0
        invoices_total = 0

        for invoice in invoices:
            invoice_id, invoice_title, invoice_discount = invoice.id, invoice.title, invoice.discount

            lines = await self.invoice_repository.get_invoice_lines(invoice_id)

            subtotal = sum(line.quantity * line.price_per_one for line in lines)
            total = subtotal - (subtotal * invoice_discount)

            if total_sum_gte is not None and total < total_sum_gte:
                continue
            if total_sum_lte is not None and total > total_sum_lte:
                continue

            invoices_list.append(
                {
                    "title": invoice_title,
                    "subtotal": str(subtotal),
                    "total": str(total),
                    "lines": lines,
                }
            )

            invoices_count += 1
            invoices_total += total

        return {
            "invoices": invoices_list,
            "invoices_count": invoices_count,
            "invoices_total": str(invoices_total),
        }
