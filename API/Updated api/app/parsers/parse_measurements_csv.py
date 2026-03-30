import csv
from io import StringIO
from datetime import datetime
from typing import List
from app.models.parsed_data.measurement_data import MeasurementData

def parse_measurement_csv(
    raw_text: str
)   -> List[MeasurementData]:
    
    rows = []
    reader = csv.DictReader(StringIO(raw_text))
    
    for index, row in enumerate(reader, start=1):
        try:
            rows.append(
                MeasurementData(
                    id = index,
                    eining = row["eining_heiti"],
                    tegund = row["tegund_maelingar"],
                    sendandi = row["sendandi_maelingar"],
                    timi = datetime.fromisoformat(row["timi"]),
                    gildi_kwh = float(row["gildi_kwh"]),
                    notandi = row["notandi_heiti"]
                )
            )
        except Exception:
            continue

    return rows