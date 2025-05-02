from uuid import uuid4
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.parcels import ParcelCreate, ParcelOut
from src.repositories.parcels import (
    get_user_parcels,
    create_parcel,
    get_parcel_by_id,
    get_parcels_without_delivery_cost,
    update_parcel_cost
)

from src.services.currency import get_usd_rate
from src.services.delivery_logger import log_delivery

async def list_user_parcels(
        session: AsyncSession,
        session_id: str,
        filters: dict,
        limit: int,
        offset: int
):
    rows  = await get_user_parcels(session, session_id, filters, limit, offset)
    return [
        ParcelOut(
            **row.Parcel.__dict__,
            parcel_type_name=row.parcel_type_name
        ) for row in rows
    ]

async def register_new_parcel(
        session: AsyncSession,
        session_id: str | None,
        data: ParcelCreate
):
    if session_id is None:
        session_id = str(uuid4())

    parcel_data = {
        "name": data.name,
        "weight_kg": data.weight_kg,
        "content_cost_usd": data.content_cost_usd,
        "parcel_type_id": data.parcel_type_id,
        "session_id": session_id
    }

    parcel = await create_parcel(session, parcel_data)
    return parcel, session_id

async def get_user_parcel_by_id(
        session: AsyncSession,
        parcel_id: str,
        session_id: str
):
    row = await get_parcel_by_id(session, parcel_id, session_id)

    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcel not found")

    return ParcelOut(
        **row.Parcel.__dict__,
        parcel_type_name=row.parcel_type_name
    )

async def calculate_delivery_cost(session):
    usd_rate = await get_usd_rate()
    parcels = await get_parcels_without_delivery_cost(session)

    for parcel in parcels:
        cost = round((parcel.weight_kg * 0.5 + parcel.content_cost_usd * 0.01) * usd_rate, 2)
        await update_parcel_cost(session, parcel, cost)
        await log_delivery(parcel, usd_rate, cost)

    await session.commit()
    return len(parcels)
