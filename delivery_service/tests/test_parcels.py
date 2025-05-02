import pytest
from httpx import AsyncClient


async def _create_parcel(client: AsyncClient, name: str = "Test") -> dict:
    payload = {
        "name": name,
        "weight_kg": 2.5,
        "parcel_type_id": 1,
        "content_cost_usd": 100,
    }
    resp = await client.post("/parcels/", json=payload)
    resp.raise_for_status()
    return resp.json()


@pytest.mark.asyncio
async def test_register_parcel(client: AsyncClient):
    parcel = await _create_parcel(client, "RegisterTest")

    assert parcel["name"] == "RegisterTest"
    assert parcel["weight_kg"] == 2.5
    assert parcel["content_cost_usd"] == 100
    assert parcel["parcel_type_id"] == 1
    assert parcel["delivery_cost_rub"] is None


@pytest.mark.asyncio
async def test_get_parcels(client: AsyncClient):
    # создаём посылку, чтобы точно было что вернуть
    await _create_parcel(client, "ListTest")

    resp = await client.get("/parcels/")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list) and len(data) >= 1


@pytest.mark.asyncio
async def test_get_parcel_by_id(client: AsyncClient):
    created = await _create_parcel(client, "DetailTest")
    parcel_id = created["id"]

    resp = await client.get(f"/parcels/{parcel_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == parcel_id
