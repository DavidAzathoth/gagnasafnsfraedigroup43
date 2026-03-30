from sqlalchemy import Column, Integer, String
from app.db.base import Base

class EigendurEininga(Base):
    __tablename__ = "eigendur_eininga"
    __table_args__ = {"schema": "raforka_updated"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    heiti = Column(String(100), nullable=False)
