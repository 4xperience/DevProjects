from fastapi import APIRouter, Depends, Request, Query
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.schemas.parcels import ParcelCreate, ParcelOut
from src.db.session import get_session
from src.services.parcels import list_user_parcels, register_new_parcel, get_user_parcel_by_id
from src.core.celery_app import celery_app

router = APIRouter()

@router.get("/", response_model=list[ParcelOut])
async def get_parcels(
    request: Request,
    session: AsyncSession = Depends(get_session),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    parcel_type_id: int | None = None,
    has_delivery_cost: bool | None = None
):
    session_id = request.session.get("user_id")
    if not session_id:
        return []

    filters = {
        "parcel_type_id": parcel_type_id,
        "has_delivery_cost": has_delivery_cost
    }

    return await list_user_parcels(session, session_id, filters, limit, offset)

@router.post("/", response_model=ParcelOut)
async def register_parcel(
    data: ParcelCreate,
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    parcel, new_session_id = await register_new_parcel(
        session=session,
        session_id=request.session.get("user_id"),
        data=data
    )

    request.session["user_id"] = new_session_id
    return parcel

@router.get("/{id}", response_model=ParcelOut)
async def get_parcel_by_id(
    id: UUID,
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    session_id = request.session.get("user_id")
    if not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session not initialized")

    return await get_user_parcel_by_id(session, id, session_id)

@router.post("/calculate-delivery", status_code=status.HTTP_200_OK)
async def trigger_cost_calculation():
    celery_app.send_task("src.tasks.calculate_delivery_cost")
    return {"message": "Task has been added to the queue"}
