import traceback

from fastapi import FastAPI, APIRouter, Body, Request, Depends
from sqlalchemy.orm import Session

from app.db_core.db_connect import get_db_session
from app.schema.auth_schema import UserInfo
from app.schema.const_schema import ManagerCode, ManagerResponse
from app.operator import op_auth

router = APIRouter()


@router.post('/register', name="register new users")
# todo 管理员权限-创建用户
async def post_register_user(
        request: Request,
        user_info: UserInfo = Body(..., description="user info"),
        db_session: Session = Depends(get_db_session)
):
    response_status = ManagerCode.Success
    try:
        response_status = await op_auth.register_user(user_info, db_session)
    finally:
        return ManagerResponse(**response_status.__dict__)

# @router.post()
# # todo 管理员权限-修改密码
