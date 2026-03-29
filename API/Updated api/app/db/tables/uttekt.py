from sqlalchemy import Column, Integer, ForeignKey
from app.db.base import Base

class Uttekt(Base):
    __tablename__ = "uttekt"
    __table_args__ = {"schema": "raforka_updated"}

    mealing_id = Column(Integer, ForeignKey("raforka_updated.orkumaelingar.id"), primary_key=True)
    notandi_id =Column(Integer, ForeignKey("raforka_updated.notendur_skraning.id"), nullable=False)
