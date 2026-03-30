from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from app.db.base import Base

class NotendurSkraning(Base):
    __tablename__ = "notendur_skraning"
    __table_args__ = {"schema": "raforka_updated"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    heiti = Column(String(100), nullable=False)
    ar_stofnad = Column(Integer, nullable=False)
    X_HNIT = Column("X_HNIT", Numeric(9, 6), nullable=False)
    Y_HNIT = Column("Y_HNIT", Numeric(9, 6), nullable=False)
    eigandi_id = Column(Integer, ForeignKey("raforka_updated.eigendur_notenda.id"))