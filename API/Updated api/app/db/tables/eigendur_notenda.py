from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class EigendurNotenda(Base):
    __tablename__ = "eigendur_notenda"
    __table_args__ = {"schema": "raforka_updated"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    kennitala = Column(String(10), unique=True, nullable=False)
    heiti = Column(String(100), nullable=False)