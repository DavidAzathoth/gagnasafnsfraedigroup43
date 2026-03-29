from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, Numeric
from app.db.base import Base

class OrkuMaelingar(Base):
    __tablename__ = "orku_maelingar"
    __table_args__ = {"schema": "raforka_updated"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    eining_id = Column(Integer, ForeignKey("raforka_updated.orku_einingar"), nullable=False)
    tegund = Column(String(11), CheckConstraint(
        "LOWER(tegund) IN ('framleiðsla', 'innmötun', 'úttekt')",
        name="check_tegund_valid"
    ), nullable=False)
    timi = Column(DateTime, nullable=False)
    gildi_kwh = Column(Numeric, nullable=False)
