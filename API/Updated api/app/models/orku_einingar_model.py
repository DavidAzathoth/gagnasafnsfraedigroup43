from datetime import date
from pydantic import BaseModel
from typing import Optional

class OrkuEiningarModel(BaseModel):
    id: Optional[int] = None
    heiti: str
    tegund: str
    eigandi_id: Optional[int] = None
    ar_uppsett: date
    X_HNIT: float
    Y_HNIT: float
    tengd_stod: Optional[int] = None