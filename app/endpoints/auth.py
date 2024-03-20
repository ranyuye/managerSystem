from fastapi import FastAPI, APIRouter, Body

router = APIRouter()

@router.post('/register', name="register new users")
async def post_register_user(

):
