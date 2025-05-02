import math
import pytest
from httpx import AsyncClient

from src.services.parcels import calculate_delivery_cost


@pytest.mark.asyncio
async def test_calculate_delivery_cost(client: AsyncClient, session, monkeypatch):
    # фиктивный курс и логгер
    async def _fake_rate() -> float:
        return 100.0

    async def _fake_log(*_args, **_kwargs):
        return None

    monkeypatch.setattr("src.services.parcels.get_usd_rate", _fake_rate)
    monkeypatch.setattr("src.services.parcels.log_delivery", _fake_log)

    payload = {
        "name": "CalcTest",
        "weight_kg": 3.0,
        "parcel_type_id": 1,
        "content_cost_usd": 50.0,
    }

    # регистрируем посылку
    create = await client.post("/parcels/", json=payload)
    parcel_id = create.json()["id"]

    # считаем стоимость напрямую (без Celery/Redis)
    await calculate_delivery_cost(session)

    # проверяем результат
    resp = await client.get(f"/parcels/{parcel_id}")
    parcel = resp.json()

    expected = round(
        (payload["weight_kg"] * 0.5 + payload["content_cost_usd"] * 0.01) * 100.0,
        2,
    )
    assert math.isclose(parcel["delivery_cost_rub"], expected, rel_tol=1e-2)
