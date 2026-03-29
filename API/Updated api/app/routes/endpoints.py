# Task C5
from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.db.session import get_orkuflaedi_session
from sqlalchemy.orm import Session
from app.services.service import (
    get_orku_einingar_data,
    get_monthly_energy_flow_data,
    get_monthly_company_usage_data,
    get_monthly_plant_ross_ratios_data,
)
from app.utils.validate_date_range import validate_date_range_helper
from datetime import datetime

router = APIRouter()
db_name = "OrkuFlaediIsland"

@router.get("/monthly-energy-flow")
def get_monthly_energy_flow(
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    db: Session = Depends(get_orkuflaedi_session)
):
    print(f"CALLING [GET] /{db_name}/monthly-energy-flow")
    from_date, to_date = validate_date_range_helper(
        from_date,
        to_date,
        datetime(2025, 1, 1, 0, 0),
        datetime(2026, 1, 1, 0, 0)
    )
    result = get_monthly_energy_flow_data(db, from_date, to_date)
    return result





'''
Endpoint 1: get_monthly_energy_flow()
'''

'''
Endpoint 2: get_monthly_company_usage()
'''

'''
Endpoint 3: get_monthly_plant_loss_ratios()
'''

# Task E1

'''
Endpoint 4: insert_measurements()
'''

# Task F1
'''
Endpoint 5: get_substations_gridflow()
'''