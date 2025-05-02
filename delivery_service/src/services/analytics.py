from datetime import datetime, UTC
from src.db.mongo import logs_collection

async def aggregate_delivery_costs_today():
    start = datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)

    pipeline = [
        {
            "$match": {
                "calculated_at": { "$gte": start }
            }
        },
        {
            "$group": {
                "_id": "$parcel_type_id",
                "total_cost": { "$sum": "$delivery_cost_rub" }
            }
        },
        {
            "$project": {
                "parcel_type_id": "$_id",
                "total_cost": { "$round": ["$total_cost", 2] },
                "_id": 0
            }
        }
    ]

    cursor = logs_collection.aggregate(pipeline)
    return [doc async for doc in cursor]
