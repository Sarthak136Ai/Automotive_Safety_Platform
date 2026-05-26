from sqlalchemy import Column, Integer, String, Text, Float
from backend.app.database.database import Base

class Recall(Base):
    __tablename__ = "recalls"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(String(50), unique=True, index=True, nullable=False)
    nhtsa_record_id = Column(String(50), index=True, nullable=True)
    manufacturer = Column(String(100), index=True, nullable=False)
    component = Column(String(100), index=True, nullable=False)
    summary = Column(Text, nullable=False)
    consequence = Column(Text, nullable=True)
    remedy = Column(Text, nullable=True)
    model_year = Column(Integer, index=True, nullable=False)
    risk_label = Column(String(20), index=True, nullable=False)
    ai_summary = Column(Text, nullable=True)
    vehicle_make = Column(String(100), index=True, nullable=True)
    vehicle_model = Column(String(100), index=True, nullable=True)
    defect_severity_score = Column(Float, default=0.0)
    recall_risk_score = Column(Float, default=0.0)
