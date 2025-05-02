from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from src.api import parcels, parcel_types, analytics
from src.core.config import settings

app = FastAPI(title="International Delivery Service")
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET)

app.include_router(parcel_types.router, prefix="/parcel-types", tags=["Parcel Types"])
app.include_router(parcels.router, prefix="/parcels", tags=["Parcels"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
