from pydantic import BaseModel
from typing import Optional

class EigendurNotendaModel(BaseModel):
    id: int
    kennitala: str
    heiti: str