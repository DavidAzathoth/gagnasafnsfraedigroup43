from pydantic import BaseModel
from typing import Optional
from datetime import date
class OrkuMaelingarModel(BaseModel):
    id: Optional[int] = None
    eining_id: int
    tegund: str
    timi: date
    gildi_kwh: float