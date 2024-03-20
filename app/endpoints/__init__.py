from fastapi import FastAPI, APIRouter

from app.endpoints import auth
router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["User Manager"])
