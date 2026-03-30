from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from app.db.base import Base

class OrkuEiningar(Base):
    __tablename__ = "orku_einingar"
    __table_args__ = {"schema": "raforka_updated"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    heiti = Column(String(100), nullable=False)
    tegund = Column(String(100), nullable=False)
    eigandi_id = Column(Integer, ForeignKey("raforka_updated.eigendur_eininga.id"), nullable=True)
    ar_uppsett = Column(Date, nullable=False)
    X_HNIT = Column(Numeric(9, 6), nullable=False)
    Y_HNIT = Column(Numeric(9, 6), nullable=False)
    tengd_stod = Column(Integer, ForeignKey("raforka_updated.orku_einingar.id"), nullable=True)