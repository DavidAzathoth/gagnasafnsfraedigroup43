from pydantic import BaseModel
from typing import Optional

class NotendurSkraningModel(BaseModel):
    id: Optional[int] = None
    heiti: str
    ar_stofnad: int
    X_HNIT: float
    Y_HNIT: float
    eigandi_id: Optional[int] = None