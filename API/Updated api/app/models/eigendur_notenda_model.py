from pydantic import BaseModel
from typing import Optional

class EigendurNotendaModel(BaseModel):
    id: Optional[int] = None
    kennitala: str
    heiti: str