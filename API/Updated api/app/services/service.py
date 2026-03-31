# Task C5
from datetime import datetime
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.tables.eigendur_notenda import EigendurNotenda
from app.models.eigendur_notenda_model import EigendurNotendaModel
from app.db.tables.eigendur_eininga import EigendurEininga
from app.models.eigendur_notenda_model import EigendurNotendaModel
from app.db.tables.notendur_skraning import NotendurSkraning
from app.models.notendur_skraning_model import NotendurSkraningModel
from app.db.tables.orku_einingar import OrkuEiningar
from app.models.orku_einingar_model import OrkuEiningarModel
from app.db.tables.orku_maelingar import OrkuMaelingar
from app.models.orku_maelingar_model import OrkuMaelingarModel
from app.db.tables.uttekt import Uttekt
from app.models.uttekt_model import UttektModel
from app.models.monthly_energy_flow_model import MonthlyPlantEnergyFlowModel
from app.models.monthly_company_usage_model import MonthlyCompanyUsageModel
from app.models.monthly_plant_loss_ratios import MonthlyPlantLossRatiosModel
from app.models.parsed_data.measurement_data import MeasurementData
from app.utils.validate_file_type import validate_file_type
from app.parsers.parse_measurements_csv import parse_measurement_csv

def get_orku_einingar_data(
    db: Session,
    from_date: datetime,
    to_date: datetime
):
    rows = db.query(OrkuEiningar).all()

    return [
        OrkuEiningarModel(
            id=row.id,
            heiti=row.heiti,
            tegund=row.tegund,
            eigandi_id=row.eigandi_id,
            ar_uppsett=row.ar_uppsett,
            X_HNIT = row.X_HNIT,
            Y_HNIT = row.Y_HNIT,
            tengd_stod = row.tengd_stod,
        ) 
        for row in rows
    ]

'''
Service 1: get_monthly_energy_flow_data()
'''
def get_monthly_energy_flow_data(
    db: Session,
    from_date: datetime,
    to_date: datetime
):
    try:
        query = """
        SELECT * 
        FROM raforka_updated.monthly_energy_flow_data
        WHERE MAKE_DATE(year::int, month::int, 1)
            BETWEEN :from_date AND :to_date
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
    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

'''
Service 2: get_monthly_company_usage_data()
'''

def get_monthly_company_usage_data(
        db: Session,
        from_date: datetime,
        to_date: datetime
):
    query = """
    SELECT *
    FROM raforka_updated.yearly_usage_by_company
    WHERE MAKE_DATE(year::int, month::int, 1)
        BETWEEN :from_date AND :to_date
"""
    try:
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
    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

'''
Service 3: get_monthly_plant_loss_ratios_data()
'''

def get_monthly_plant_loss_ratios_data(
        db: Session,
        from_date: datetime,
        to_date: datetime
):

    query = """
    SELECT
        power_plant_source,
        AVG((production_kwh - inflow_kwh) / production_kwh) AS plant_to_sub_loss_ratio,
        AVG((production_kwh - withdrawal_kwh) / production_kwh) AS total_system_loss_ratio
    FROM raforka_updated.montly_power_plant_energy_view
    WHERE MAKE_DATE(year::int, month::int, 1)
        BETWEEN :from_date AND :to_date
    GROUP BY power_plant_source
    ORDER BY power_plant_source ASC;
"""
    rows = db.execute(
        text(query),
            {
                "from_date": from_date,
                "to_date": to_date,
            }
        ).mappings().all()

    return [
        MonthlyPlantLossRatiosModel(
            power_plant_source = row.power_plant_source,
            plant_to_substation_loss_ratio = row.plant_to_sub_loss_ratio,
            total_system_loss_ratio = row.total_system_loss_ratio
        )
        for row in rows
    ]
# Task E1

'''
Service 4: insert_measurements_data()
'''
async def insert_measurement_data(
        file: UploadFile,
        db: Session,
        mode: str = "bulk"
):
    validate_file_type(
        file,
        allowed_extensions=[".csv"]
    )
    einingar = db.execute(text("""
        SELECT id, heiti FROM raforka_updated.orku_einingar""")).all()
    eining_map = {row.heiti: row.id for row in einingar}
    notendur = db.execute(text("""
        SELECT ns.id, en.heiti FROM raforka_updated.notendur_skraning ns
        JOIN raforka_updated.eigendur_notenda en ON en.id = ns.eigandi_id
""")).all()
    notendur_map = {row.heiti: row.id for row in notendur} #Might be a problem when companies own multiple users


    raw_data = await file.read()
    raw_text = raw_data.decode()

    parsed_rows: list[MeasurementData]
    parsed_rows = parse_measurement_csv(raw_text)

    if not parsed_rows:
        raise HTTPException(status_code=400, detail="No valid rows found")

    try:
        if mode in ("single"): #Can't seem to find a way to bulk insert without losing references to maeling ids for uttekt table
            for row in parsed_rows:
                measurement = OrkuMaelingar(
                    eining_id = eining_map[row.eining],
                    tegund = row.tegund,
                    timi = row.timi,
                    gildi_kwh = row.gildi_kwh
                )
                db.add(measurement)
                db.flush()

                if row.notandi:
                    db.add(
                        Uttekt(
                            maeling_id = measurement.id,
                            notandi_id = notendur_map[row.notandi]
                        )
                    )
                    db.flush()
            db.rollback() #testing
            db.commit()
        elif mode == "bulk": #cant use bulk_insert_mappings without losing reference to maeling ids for uttekts. So i do 1000 at a time
            measurements = [] # measurements and batch_rows are used to reference maeling_ids for uttekts
            batch_rows = []
            
            for row in parsed_rows:
                measurement = OrkuMaelingar(
                    eining_id = eining_map[row.eining],
                    tegund = row.tegund,
                    timi = row.timi,
                    gildi_kwh = row.gildi_kwh
                )
                measurements.append(measurement)
                batch_rows.append(row)

                if len(measurements) >= 1000:
                    db.add_all(measurements)
                    db.flush()
                
                    uttektir = []
                    for i in range(len(measurements)):
                        m = measurements[i]
                        row2 = batch_rows[i]

                        if row2.notandi:
                            uttektir.append(
                                Uttekt(
                                    maeling_id = m.id,
                                    notandi_id = notendur_map[row2.notandi]
                                )
                            )
                    if uttektir:
                        db.add_all(uttektir)
                    measurements = []
                    batch_rows = []
            if measurements:
                db.add_all(measurements)
                db.flush()

                uttektir = []
                for i in range(len(measurements)):
                    m = measurements[i]
                    row2 = batch_rows[i]

                    if row2.notandi:
                        uttektir.append(
                            Uttekt(
                                maeling_id=m.id,
                                notandi_id=notendur_map[row2.notandi]
                            )
                        )
                if uttektir:
                    db.add_all(uttektir)

            db.commit()

        elif mode == "fallback":
            for row in parsed_rows:
                try:
                    measurement = OrkuMaelingar(
                    eining_id = eining_map[row.eining],
                    tegund = row.tegund,
                    timi = row.timi,
                    gildi_kwh = row.gildi_kwh
                    )
                    db.add(measurement)
                    db.flush()
                    if row.notandi: 
                        db.add(
                            Uttekt(
                            maeling_id = measurement.id,
                            notandi_id = notendur_map[row.notandi]
                        )
                        )
                        db.flush()
                except Exception:
                    db.rollback()
                    continue
            db.commit()
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    db.execute(text("REFRESH MATERIALIZED VIEW raforka_updated.monthly_energy_flow_data"))
    db.execute(text("REFRESH MATERIALIZED VIEW raforka_updated.yearly_usage_by_company"))
    db.execute(text("REFRESH MATERIALIZED VIEW raforka_updated.montly_power_plant_energy_view"))
    db.commit() #update materialized views
    return {
        "status": 200,
        "rows_processed": len(parsed_rows),
        "mode": mode
    }
# Task F1


'''
Service 5: get_substations_gridflow_data()
'''