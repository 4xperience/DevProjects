import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_parcel_types(client: AsyncClient):
    resp = await client.get("/parcel-types/")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list) and len(data) >= 3

    names = {item["name"] for item in data}
    assert {"одежда", "электроника", "разное"}.issubset(names)
