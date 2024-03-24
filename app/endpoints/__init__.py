from fastapi import FastAPI, APIRouter

from app.endpoints import auth, dept
router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["User Manager"])
router.include_router(dept.router, prefix="/dept", tags=["Dept Manager"])
