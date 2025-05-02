from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models import ParcelType
from src.db.session import get_session
from pydantic import BaseModel

router = APIRouter()

class ParcelTypeOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

@router.get("/", response_model=list[ParcelTypeOut])
async def get_parcel_types(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ParcelType))
    return result.scalars().all()
