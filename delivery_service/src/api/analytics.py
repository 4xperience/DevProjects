from fastapi import APIRouter
from src.services.analytics import aggregate_delivery_costs_today

router = APIRouter()

@router.get("/daily-costs")
async def get_daily_costs_by_type():
    return await aggregate_delivery_costs_today()
