import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Optional

from app.db_core.db_model import Dept, DeptRelation
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


async def dept_list(db_session: Session) -> (ManagerCode, dict):
    """
    :param db_session:
    :return:  (ManagerCode, dict)
    """
    response_status, data = ManagerCode.Success, {}
    try:




