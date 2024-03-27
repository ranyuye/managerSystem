import logging
import traceback

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased
from typing import Optional

from app.db_core.db_model import Dept, DeptRelation, Users
from app.schema.const_schema import ManagerCode
from app.schema.dept_schema import DeptInfo, DeptUpdateInfo
from app.schema.error_schema import DataNotExist
from app.utils.format_time import now


async def create_dept(dept_info: DeptInfo, db_session: Session) -> (ManagerCode, int):
    """
    :param db_session:
    :param dept_info:
    :param db_session:
    :return: Optional[ManagerCode, int]
    """
    response_status, dept_id = ManagerCode.Success, None
    try:
        dept_insert = Dept(
            name=dept_info.dept_name,
            leader=dept_info.dept_leader
        )
        db_session.add(dept_insert)
        logging.info(f"insert dept id: {dept_insert.id}")
        if dept_info.dept_parent:
            exist_parent_dept = db_session.query(Dept).filter(Dept.id == dept_info.dept_parent).first()
            if not exist_parent_dept:
                raise DataNotExist
            dept_relation = DeptRelation(
                child_dept_id=dept_insert.id,
                parent_dept_id=dept_info.dept_parent
            )
            db_session.add(dept_relation)
            logging.info(f"insert dept relation id: {dept_relation.id}")
        db_session.commit()
        dept_id = dept_insert.id
    except SQLAlchemyError as e:
        logging.error(f"Error while create_dept dept: {e}")
        response_status, dept_id = ManagerCode.DataBaseError, None
    except DataNotExist as e:
        logging.error(f"DataNotExist while create_dept dept: {e}")
        response_status, dept_id = ManagerCode.DeptNotExist, None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        response_status, dept_id = ManagerCode.UnknownError, None
    finally:
        return response_status, dept_id


async def update_dept(dept_info: DeptUpdateInfo, db_session: Session) -> ManagerCode:
    """
    :param db_session:
    :param dept_info:
    :return: ManagerCode
    """
    response_status = ManagerCode.Success
    try:
        update_info = db_session.query(Dept).filter(Dept.id == dept_info.id, Dept.status == 1).update(
            {
                Dept.name: dept_info.dept_name,
                Dept.leader: dept_info.dept_leader,
                Dept.status: dept_info.status,
                Dept.update_time: now()
            }
        )
        if update_info == 0:
            raise DataNotExist
        if dept_info.dept_parent:
            exist_parent_dept = db_session.query(Dept).filter(Dept.id == dept_info.dept_parent).first()
            if not exist_parent_dept:
                raise DataNotExist
            exist_relation = db_session.query(DeptRelation).filter(DeptRelation.child_dept_id == dept_info.id,
                                                                   DeptRelation.status == 1).first()
            if exist_relation and exist_relation.parent_dept_id == dept_info.dept_parent:
                return

            db_session.query(DeptRelation).filter(DeptRelation.id == exist_relation.id).update(
                {
                    DeptRelation.status: -1,
                    DeptRelation.update_time: now()
                }
            )
            dept_relation = DeptRelation(
                child_dept_id=dept_info.id,
                parent_dept_id=dept_info.dept_parent
            )
            db_session.add(dept_relation)
        db_session.commit()
    except SQLAlchemyError as e:
        logging.error(f"Error while update_dept dept: {e}")
        response_status = ManagerCode.DataBaseError
    except DataNotExist as e:
        logging.error(f"DataNotExist while update_dept dept: {e}")
        response_status = ManagerCode.DeptNotExist
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        response_status = ManagerCode.UnknownError
    finally:
        return response_status


async def dept_list(db_session: Session, dept_id: int, dept_name: str, dept_parent: int, page: int, size: int,
                    export: bool = False) -> (ManagerCode, dict):
    """
    :param export:
    :param size:
    :param dept_parent:
    :param dept_name:
    :param dept_id:
    :param page:
    :param db_session:
    :return:  (ManagerCode, dict)
    """
    response_status, data = ManagerCode.Success, {}
    try:
        with db_session as db_session:
            Parent = aliased(Dept)
            query = db_session.query(
                Dept.id, Dept.name, Dept.create_time, Dept.update_time, Users.name.label("leader_name"),
                Parent.name.label("parent_name")
            ).join(
                Users, Users.id == Dept.leader, isouter=True
            ).join(
                DeptRelation, DeptRelation.child_dept_id == Dept.id, isouter=True
            ).join(
                Parent, Parent.id == DeptRelation.parent_dept_id, isouter=True
            ).filter(
                Dept.status == 1, DeptRelation.status == 1
            ).order_by(Dept.create_time.desc())
            if dept_id:
                query = query.filter(Dept.id == dept_id)
            if dept_name:
                query = query.filter(Dept.name.like(f"%{dept_name}%"))
            if dept_parent:
                query = query.filter(DeptRelation.parent_dept_id == dept_parent)
            count: int = query.count()
            if page and size and not export:
                query = query.offset(page * size).limit(size)
            items: list = []
            for item in query.all():
                items.append(
                    {
                        "id": item.id,
                        "name": item.name,
                        "create_time": item.create_time,
                        "update_time": item.update_time,
                        "leader_name": item.leader_name,
                        "parent_name": item.parent_name
                    }
                )
            col: dict = {"id": "ID", "name": "部门名称", "leader_name": "领导", "parent_name": "上属部门",
                         "create_time": "创建时间", "update_time": "更新时间"}
            data: dict = {"items": items, "total": count, "col": col}
    except SQLAlchemyError as e:
        logging.error(f"Error while dept_list dept: {traceback.format_exc()}")
        response_status, data = ManagerCode.DataBaseError, {}
    except Exception as e:
        logging.error(f"Unexpected error: {traceback.format_exc()}")
        response_status, data = ManagerCode.UnknownError, {}
    finally:
        return response_status, data



