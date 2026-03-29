from pydantic import BaseModel
from typing import Optional

class UttektModel(BaseModel):
    mealing_id: Optional[int] = None
    notandi_id: Optional[int] = None

