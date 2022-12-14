from fastapi import APIRouter

from app.routers.api.v1.locations import router as location_router


router = APIRouter()
router.include_router(location_router)
