from pydantic import BaseModel
from typing import Optional

class EigendurEiningaModel(BaseModel):
    id: Optional[int] = None
    heiti: str