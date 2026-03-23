from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.tables.orku_einingar import OrkuEiningar
from app.models.orku_einingar_model import OrkuEiningarModel
from app.db.tables.notendur_skraning import NotendurSkraning
from app.models.notendur_skraning_model import NotendurSkraningModel
from app.db.tables.orku_maelingar import OrkuMaelingar
from app.models.orku_maelingar_model import OrkuMaelingarModel
from app.models.monthly_energy_flow_model import MonthlyPlantEnergyFlowModel
from app.models.monthly_company_usage_model import MonthlyCompanyUsageModel
from app.models.monthly_plant_loss_ratios import MonthlyPlantLossRatiosModel
from app.db.tables.test_measurement import TestMeasurement
from app.models.parsed_data.test_measurement_data import TestMeasurementData
from app.parsers.parse_test_measurment_csv import parse_test_measurement_csv
from app.utils.validate_file_type import validate_file_type
from datetime import datetime

'''
Services already in place
'''
def get_orku_einingar_data(
    db: Session
):
    rows = db.query(OrkuEiningar).all()

    return [
        OrkuEiningarModel(
            id=row.id,
            heiti=row.heiti,
            tegund=row.tegund,
            tegund_stod=row.tegund_stod,
            eigandi=row.eigandi,
            ar_uppsett=row.ar_uppsett,
            manudir_uppsett=row.manudir_uppsett,
            dagur_uppsett=row.dagur_uppsett,
            X_HNIT=row.X_HNIT,
            Y_HNIT=row.Y_HNIT,
            tengd_stod=row.tengd_stod,
        ) 
        for row in rows
    ]

def get_notendur_skraning_data(
    db: Session
):
    rows = db.query(NotendurSkraning).all()

    return [
        NotendurSkraningModel(
            id=row.id,
            heiti=row.heiti,
            kennitala=row.kennitala,
            eigandi=row.eigandi,
            ar_stofnad=row.ar_stofnad,
            X_HNIT=row.X_HNIT,
            Y_HNIT=row.Y_HNIT,
        ) 
        for row in rows
    ]

def get_orku_maelingar_data(
    from_date: datetime,
    to_date: datetime,
    limit: int,
    offset: int,
    db: Session,
    eining: str | None = None,
    tegund: str | None = None,
):
    query = db.query(OrkuMaelingar).filter(
        OrkuMaelingar.timi >= from_date,
        OrkuMaelingar.timi <= to_date
    )

    if eining:
        query = query.filter(OrkuMaelingar.eining_heiti == eining)
    if tegund:
        query = query.filter(OrkuMaelingar.tegund_maelingar == tegund)

    rows = (
        query
        .order_by(OrkuMaelingar.timi)
        .limit(limit)
        .offset(offset)
        .all()
    )

    return [
        OrkuMaelingarModel(
            id=row.id,
            eining_heiti=row.eining_heiti,
            tegund_maelingar=row.tegund_maelingar,
            sendandi_maelingar=row.sendandi_maelingar,
            timi=row.timi,
            gildi_kwh=row.gildi_kwh,
            notandi_heiti=row.notandi_heiti
        )
        for row in rows
    ]

async def insert_test_measurement_data(
    file: UploadFile,
    db: Session,
    mode: str = "bulk"
):
    validate_file_type(
        file, 
        allowed_extensions=[".csv"]
    )

    raw_data = await file.read()
    raw_text = raw_data.decode()

    parsed_rows: list[TestMeasurementData]
    parsed_rows = parse_test_measurement_csv(raw_text)

    if not parsed_rows:
        raise HTTPException(status_code=400, detail="No valid rows found")

    try:
        if mode == "single":
            for row in parsed_rows:
                db.add(
                    TestMeasurement(
                        timi=row.timi,
                        value=row.value
                    )
                )
            db.commit()

        elif mode == "bulk":
            insert_data = [
                {
                    "timi": row.timi,
                    "value": row.value
                }
                for row in parsed_rows
            ]
            db.bulk_insert_mappings(TestMeasurement, insert_data)
            db.commit()

        elif mode == "fallback":
            for row in parsed_rows:
                try:
                    db.add(
                        TestMeasurement(
                            timi=row.timi,
                            value=row.value
                        )
                    )
                    db.flush()
                except Exception:
                    db.rollback()
                    continue
            db.commit()
        else:
            raise HTTPException(status_code=400, detail="Invalid mode")

        return {
            "status": 200,
            "rows_processed": len(parsed_rows),
            "mode": mode
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
# Task B2

'''
Service 1: get_monthly_energy_flow_data()
'''

def get_monthly_energy_flow_data(
        db: Session,
        from_date: datetime,
        to_date: datetime
):
    
    query = """
SELECT 
    eining_heiti as power_plant_source,
    EXTRACT(year FROM timi) as year,
    EXTRACT(month FROM timi) as month,
    tegund_maelingar as measurement_type,
    SUM(gildi_kwh) as total_kwh
FROM raforka_legacy.orku_maelingar
WHERE timi >= :from_date AND timi <= :to_date
GROUP BY
    eining_heiti,
    EXTRACT(year FROM timi),
    EXTRACT(month FROM timi),
    tegund_maelingar
ORDER BY eining_heiti, month, total_kwh DESC
    """

    rows = db.execute(
        text(query),
            {
                "from_date": from_date,
                "to_date": to_date
            }
        ).mappings().all()
    
    return [
        MonthlyPlantEnergyFlowModel(
            power_plant_source = row.power_plant_source,
            measurement_type = row.measurement_type,
            year = row.year,
            month = row.month,
            total_kwh = row.total_kwh
        )
        for row in rows
    ]

'''
Service 2: get_monthly_company_usage_data()
'''

def get_monthly_company_usage_data(
        db: Session,
        from_date: datetime,
        to_date: datetime
):

    query = """
SELECT
    eining_heiti as power_plant_source,
    EXTRACT(year FROM timi) as year,
    EXTRACT(month FROM timi) as month,
    notandi_heiti as customer_name,
    sum(gildi_kwh) as total_kwh
FROM raforka_legacy.orku_maelingar
WHERE timi >= :from_date AND timi <= :to_date
AND notandi_heiti IS NOT NULL
GROUP BY
    eining_heiti,
    EXTRACT(year from timi),
    EXTRACT(month from timi),
    notandi_heiti
ORDER BY power_plant_source, month, customer_name
"""
    rows = db.execute(
        text(query),
        {
            "from_date": from_date,
            "to_date": to_date
        }
    ).mappings().all()

    return [
        MonthlyCompanyUsageModel(
            power_plant_source = row.power_plant_source,
            customer_name = row.customer_name,
            year = row.year,
            month = row.month,
            total_kwh = row.total_kwh
        )
        for row in rows
    ]
'''
Service 3: get_monthly_plant_loss_ratios_data()
'''

def get_monthly_plant_ross_ratios_data(
        db: Session,
        from_date: datetime,
        to_date: datetime
):
    query = """
DROP VIEW IF EXISTS montly_power_plant_energy_view;

CREATE VIEW montly_power_plant_energy_view as
SELECT
    eining_heiti as power_plant_source,
    EXTRACT(YEAR FROM timi) as year,
    EXTRACT(MONTH FROM timi) as month,
    SUM(gildi_kwh) FILTER (WHERE tegund_maelingar = 'Framleiðsla') AS production_kwh,
    SUM(gildi_kwh) FILTER (WHERE tegund_maelingar = 'Innmötun') AS inflow_kwh,
    SUM(gildi_kwh) FILTER (WHERE tegund_maelingar = 'Úttekt') AS withdrawal_kwh
FROM raforka_legacy.orku_maelingar
WHERE timi >= :from_date AND timi <= :to_date
GROUP BY
    eining_heiti,
    EXTRACT(YEAR FROM timi),
    EXTRACT(MONTH FROM timi);

SELECT
    power_plant_source,
    AVG((production_kwh - inflow_kwh) / production_kwh) AS plant_to_substation_loss_ratio,
    AVG((production_kwh - withdrawal_kwh) / production_kwh) AS total_system_loss_ratio
FROM montly_power_plant_energy_view
GROUP BY power_plant_source
ORDER BY power_plant_source ASC;
"""
    rows = db.execute(
        text(query),
        {
            "from_date": from_date,
            "to_date": to_date
        }
    ).mappings().all()

    return [
        MonthlyPlantLossRatiosModel(
            power_plant_source = row.power_plant_source,
            plant_to_substation_loss_ratio = row.plant_to_substation_loss_ratio,
            total_system_loss_ratio = row.total_system_loss_ratio
        )
        for row in rows
    ]