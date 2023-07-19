from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_async_session
from schemas import InvoiceOutSchema
from src.dependencies import PaginationParams
from src.repository import InvoiceRepository
from src.service import InvoiceService

app = FastAPI()


@app.get("/invoices/", response_model=List[InvoiceOutSchema])
async def get_invoices(
        pagination: PaginationParams = Depends(),
        session: AsyncSession = Depends(get_async_session),
):
    invoice_repository = InvoiceRepository(session)
    invoice_service = InvoiceService(invoice_repository)
    return await invoice_service.get_invoices_with_totals(
        pagination.skip,
        pagination.limit,
        pagination.total_sum_gte,
        pagination.total_sum_lte,
    )
