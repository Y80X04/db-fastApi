from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OperationCreate(BaseModel):
    quantity: str
    figi: str
    instrument_type: Optional[str] = None
    date: datetime
    type: str
