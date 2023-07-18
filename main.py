from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import Invoice, InvoiceLine, get_async_session

app = FastAPI()


@app.get("/invoices/", response_model=list[dict])
async def get_invoices(
        session: AsyncSession = Depends(get_async_session),
        skip: int = Query(
            0, ge=0
        ),  # Параметр для пропуска определенного количества инвойсов
        limit: int = Query(
            100, ge=1
        ),  # Параметр для ограничения количества инвойсов на странице
        total_sum_gte: Optional[float] = Query(
            None, ge=0
        ),  # Фильтр по сумме больше или равно
        total_sum_lte: Optional[float] = Query(
            None, ge=0
        ),  # Фильтр по сумме меньше или равно
):
    # Подготовка запроса для получения списка инвойсов
    invoices_query = select(Invoice.id, Invoice.title, Invoice.discount)
    invoices_results = await session.execute(invoices_query)
    invoices = invoices_results.all()
    invoices_list = []
    invoices_count = 0
    invoices_total = 0
    for invoice in invoices:
        invoice_id, invoice_title, invoice_discount = invoice
        # Подготовка запроса для получения списка линий для каждого инвойса
        lines_query = select(
            InvoiceLine.title,
            InvoiceLine.quantity,
            InvoiceLine.price_per_one,
            (InvoiceLine.quantity * InvoiceLine.price_per_one).label("subtotal_line"),
        ).where(InvoiceLine.id == invoice_id)
        lines_results = await session.execute(lines_query)
        lines = lines_results.all()
        subtotal = sum(line["subtotal_line"] for line in lines)
        total = subtotal - (subtotal * invoice_discount)
        # Фильтрация по сумме
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
        # Ограничение по пагинации
        if invoices_count >= limit:
            break
    return {
        "invoices": invoices_list[skip: skip + limit],
        "invoices_count": invoices_count,
        "invoices_total": str(invoices_total),
    }
