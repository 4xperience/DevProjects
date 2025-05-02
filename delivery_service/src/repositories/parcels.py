from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Parcel, ParcelType

async def get_user_parcels(
        session: AsyncSession,
        session_id: str,
        filters: dict,
        limit: int,
        offset: int
        ):
    conditions = [Parcel.session_id == session_id]

    if filters.get("parcel_type_id"):
        conditions.append(Parcel.parcel_type_id == filters["parcel_type_id"])
    if filters.get("has_delivery_cost") is True:
        conditions.append(Parcel.delivery_cost_rub.isnot(None))
    elif filters.get("has_delivery_cost") is False:
        conditions.append(Parcel.delivery_cost_rub.is_(None))

    stmt = (
        select(Parcel, ParcelType.name.label("parcel_type_name"))
        .join(ParcelType)
        .where(and_(*conditions))
        .limit(limit)
        .offset(offset)
    )

    result = await session.execute(stmt)
    return result.all()

async def create_parcel(
        session: AsyncSession,
        parcel_data: dict
) -> Parcel:
    parcel = Parcel(**parcel_data)
    session.add(parcel)
    await session.commit()
    await session.refresh(parcel)
    return parcel

async def get_parcel_by_id(
        session: AsyncSession,
        parcel_id: str,
        session_id: str
):
    stmt = (
        select(Parcel, ParcelType.name.label("parcel_type_name"))
        .join(ParcelType)
        .where(
            Parcel.id == parcel_id,
            Parcel.session_id == session_id
        )
    )

    result = await session.execute(stmt)
    row = result.first()
    return row

async def get_parcels_without_delivery_cost(session):
    stmt = select(Parcel).where(Parcel.delivery_cost_rub.is_(None))
    result = await session.execute(stmt)
    return result.scalars().all()

async def update_parcel_cost(session, parcel: Parcel, cost: float):
    parcel.delivery_cost_rub = cost
    session.add(parcel)
