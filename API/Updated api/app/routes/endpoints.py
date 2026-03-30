# Task C5
from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.db.session import get_orkuflaedi_session
from sqlalchemy.orm import Session
from app.services.service import (
    get_orku_einingar_data,
    get_monthly_energy_flow_data,
    get_monthly_company_usage_data,
    get_monthly_plant_loss_ratios_data,
    insert_measurement_data,
)
from app.utils.validate_date_range import validate_date_range_helper
from datetime import datetime





'''
Endpoint 1: get_monthly_energy_flow()
'''
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
Endpoint 2: get_monthly_company_usage()
'''
@router.get("/monthly-company-usage")
def get_monthly_company_usage(
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    db: Session = Depends(get_orkuflaedi_session)
):
    print(f"CALLING [GET] /{db_name}/monthly-company-usage")
    from_date, to_date = validate_date_range_helper(
        from_date,
        to_date,
        datetime(2025, 1, 1, 0, 0),
        datetime(2026, 1, 1, 0, 0)
    )
    result = get_monthly_company_usage_data(db, from_date, to_date)
    return result


'''
Endpoint 3: get_monthly_plant_loss_ratios()
'''
@router.get("/monthly-plant-loss-ratios")
def get_monthly_plant_loss_ratios(
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    db: Session = Depends(get_orkuflaedi_session)
):
    print(f"CALLING [GET] /{db_name}/monthly-plant-loss-ratios")
    from_date, to_date = validate_date_range_helper(
        from_date,
        to_date,
        datetime(2025, 1, 1, 0, 0),
        datetime(2026, 1, 1, 0, 0)
    )
    result = get_monthly_plant_loss_ratios_data(db, from_date, to_date)
    return result

# Task E1

'''
Endpoint 4: insert_measurements()
'''
@router.post("/insert-measurement-data")
async def insert_measurement(
    mode: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_orkuflaedi_session)
):
    print(f"CALLING [POST] /{db_name}/insert-measurement-data")

    result = await insert_measurement_data(file, db, mode)
    return result

# Task F1
'''
Endpoint 5: get_substations_gridflow()
'''