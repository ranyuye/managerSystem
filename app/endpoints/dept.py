from urllib.parse import quote

from fastapi import APIRouter, Body, Request, Depends, Query, Response
from sqlalchemy.orm import Session

from app.db_core.db_connect import get_db_session
from app.operator import op_dept
from app.schema.const_schema import ManagerCode, ManagerResponse
from app.schema.dept_schema import DeptInfo, DeptUpdateInfo
from app.utils.export_excle import create_excel

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


@router.get("/list", name="get department list")
# todo 权限-查看部门列表
async def get_dept_list(
        request: Request,
        dept_id: int = Query(None, description="dept_id"),
        dept_name: str = Query(None, description="dept_name"),
        dept_parent: int = Query(None, description="dept_parent"),
        export: bool = Query(False, description="export"),
        page: int = Query(1, description="page"),
        size: int = Query(10, description="page_size"),
        db_session: Session = Depends(get_db_session)
):
    response_status, data = await op_dept.dept_list(db_session=db_session, dept_id=dept_id, dept_name=dept_name,
                                                    dept_parent=dept_parent, page=page, size=size)
    if export and data:
        xlsx_io = create_excel(headers=data["col"], data=data["items"])
        return Response(content=xlsx_io.getvalue(),
                        headers={'Content-Disposition': f'attachment; filename="{quote("部门信息列表")}.xlsx"'},
                        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    return ManagerResponse(**{**response_status.__dict__, "data": data})
