from pydantic import BaseModel, Field
from uuid import UUID

class ParcelCreate(BaseModel):
    name: str
    weight_kg: float = Field(gt=0)
    parcel_type_id: int
    content_cost_usd: float = Field(ge=0)

class ParcelOut(BaseModel):
    id: UUID
    name: str
    weight_kg: float
    content_cost_usd: float
    parcel_type_id: int
    parcel_type_name: str | None = None
    delivery_cost_rub: float | None = None

    class Config:
        from_attributes = True
