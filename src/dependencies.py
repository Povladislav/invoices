from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    skip: int = Query(0, ge=0)
    limit: int = Query(100, ge=1)
    total_sum_gte: Optional[float] = Query(None, ge=0)
    total_sum_lte: Optional[float] = Query(None, ge=0)
