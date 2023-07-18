from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_async_session
from src.dependencies import PaginationParams
from src.repository import InvoiceRepository

app = FastAPI()


@app.get("/invoices/", response_model=list[dict])
async def get_invoices(
    pagination: PaginationParams = Depends(),
    # Get the pagination parameters from the request, using the PaginationParams dependency.
    session: AsyncSession = Depends(get_async_session),
    # Get the database session, using the get_async_session dependency.
):
    invoice_repository = InvoiceRepository(
        session
    )  # Create an instance of the InvoiceRepository, passing the database session.
    return await invoice_repository.get_invoices(
        pagination.skip,  # The number of invoices to skip, used for pagination.
        pagination.limit,  # The number of invoices to include in the response, used for pagination.
        pagination.total_sum_gte,  # Optional filter: minimum total sum for invoices.
        pagination.total_sum_lte,  # Optional filter: maximum total sum for invoices.
    )
