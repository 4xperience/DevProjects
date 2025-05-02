import asyncio
from sqlalchemy import select
from src.db.models import ParcelType
from src.db.session import async_session

INITIAL_TYPES = ["одежда", "электроника", "разное"]

async def init_parcel_types():
    async with async_session() as session:
        existing = (await session.execute(select(ParcelType.name))).scalars().all()
        for name in INITIAL_TYPES:
            if name not in existing:
                session.add(ParcelType(name=name))
        await session.commit()

if __name__ == "__main__":
    asyncio.run(init_parcel_types())
