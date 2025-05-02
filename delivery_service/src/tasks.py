from celery import shared_task
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import settings
from src.services.parcels import calculate_delivery_cost

engine = create_async_engine(settings.db_url(async_mode=True), echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)

@shared_task(name="src.tasks.calculate_delivery_cost")
def calc_delivery_task():
    import asyncio

    async def _run():
        async with async_session() as session:
            await calculate_delivery_cost(session)

    asyncio.run(_run())
    return "ok"
