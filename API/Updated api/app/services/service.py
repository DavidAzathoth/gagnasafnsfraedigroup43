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
    from_month = from_date.month
    to_month = to_date.month
    from_year = from_date.year
    to_year = to_date.year
    query = """
    SELECT * 
    FROM raforka_updated.monthly_energy_flow_data
    WHERE :from_month <= month AND month <= :to_month
    AND :from_year <= year AND year <= :to_year
    """
    rows = db.execute(
        text(query),
            {
                "from_month": from_month,
                "to_month": to_month,
                "from_year": from_year,
                "to_year": to_year
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

def get_monthly_company_usage_data():
    return None

'''
Service 3: get_monthly_plant_loss_ratios_data()
'''

def get_monthly_plant_ross_ratios_data():
    return 
# Task E1

'''
Service 4: insert_measurements_data()
'''

# Task F1

'''
Service 5: get_substations_gridflow_data()
'''