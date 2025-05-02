from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid

Base = declarative_base()

class ParcelType(Base):
    __tablename__ = "parcel_types"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Parcel(Base):
    __tablename__ = "parcels"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String, index=True, nullable=False)

    name = Column(String, nullable=False)
    weight_kg = Column(Float, nullable=False)
    content_cost_usd = Column(Float, nullable=False)

    parcel_type_id = Column(Integer, ForeignKey("parcel_types.id"), nullable=False)
    parcel_type = relationship("ParcelType")

    delivery_cost_rub = Column(Float, nullable=True)
    transport_company_id = Column(Integer, nullable=True, unique=True)
