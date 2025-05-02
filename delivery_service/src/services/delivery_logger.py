from datetime import datetime, UTC
from src.db.mongo import logs_collection

async def log_delivery(parcel, usd_rate: float, cost: float):
    await logs_collection.insert_one({
        "parcel_id": str(parcel.id),
        "session_id": parcel.session_id,
        "parcel_type_id": parcel.parcel_type_id,
        "content_cost_usd": parcel.content_cost_usd,
        "usd_rate": usd_rate,
        "delivery_cost_rub": cost,
        "calculated_at": datetime.now(UTC)
    })
