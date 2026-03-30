from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class MeasurementData:
    id: int
    eining: str
    tegund: str
    sendandi: str
    timi: datetime
    gildi_kwh: float
    notandi: str