import asyncio
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from asgi_lifespan import LifespanManager

from src.main import app
from src.db.session import engine, async_session, get_session


@pytest.fixture(scope="session", autouse=True)
def _celery_eager():
    from src.core.celery_app import celery_app

    celery_app.conf.update(
        task_always_eager=True,
        task_eager_propagates=True,
        broker_url="memory://",
        result_backend="cache+memory://",
    )
    yield
    celery_app.conf.task_always_eager = False


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def session():
    async with engine.connect() as conn:
        trans = await conn.begin()
        nested = await conn.begin_nested()

        async with async_session(bind=conn) as db:
            yield db

        await nested.rollback()
        await trans.rollback()


@pytest_asyncio.fixture(autouse=True)
async def _override_get_session(session):
    async def _get_session_override():
        yield session

    app.dependency_overrides[get_session] = _get_session_override
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="session")
async def client():
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver",
        ) as ac:
            yield ac
