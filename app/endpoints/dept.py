from fastapi import APIRouter, Body, Request, Depends
from sqlalchemy.orm import Session

from app.db_core.db_connect import get_db_session
from app.operator import op_dept
from app.schema.const_schema import ManagerCode, ManagerResponse
from app.schema.dept_schema import DeptInfo, DeptUpdateInfo

router = APIRouter()


@router.post('/create', name="create new department")
# todo 权限-创建部门
async def post_create_dept(
        request: Request,
        dept_info: DeptInfo = Body(..., description="dept info"),
        db_session: Session = Depends(get_db_session)
):
    response_status, create_id = await op_dept.create_dept(dept_info=dept_info, db_session=db_session)
    return ManagerResponse(**{**response_status.__dict__, "data": {"dept_id": create_id}})


@router.put('/update', name='update department info')
# todo 权限-编辑部门
async def pub_update_dept(
        request: Request,
        dept_info: DeptUpdateInfo = Body(..., description="dept info"),
        db_session: Session = Depends(get_db_session)
):
    response_status = await op_dept.update_dept(dept_info=dept_info, db_session=db_session)
    return ManagerResponse(**response_status.__dict__)
