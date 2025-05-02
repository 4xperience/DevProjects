import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_daily_costs_analytics(client: AsyncClient, monkeypatch):
    # подделываем ответ MongoDB-агрегации
    sample = [
        {"parcel_type_id": 1, "total_cost": 123.45},
        {"parcel_type_id": 2, "total_cost": 678.9},
    ]

    class _FakeCursor:
        def __init__(self, docs):
            self._docs = list(docs)

        def __aiter__(self):
            return self

        async def __anext__(self):
            if not self._docs:
                raise StopAsyncIteration
            return self._docs.pop(0)

    monkeypatch.setattr(
        "src.services.analytics.logs_collection.aggregate",
        lambda _pipeline: _FakeCursor(sample),
    )

    resp = await client.get("/analytics/daily-costs")
    assert resp.status_code == 200
    assert resp.json() == sample
