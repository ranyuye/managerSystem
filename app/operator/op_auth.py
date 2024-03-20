import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db_core.db_model import Users
from app.schema.auth_schema import UserInfo
from app.schema.const_schema import ManagerResponse, ManagerCode
from app.utils.jwt_auth import password_hashing


async def register_user(user_info: UserInfo, db_session: Session) -> ManagerResponse:
    """
    register user
    :param user_info:
    :param db_session:
    :return:
    """
    try:
        with db_session as db_session:
            exist_user = db_session.query(Users.id).filter(Users.email == user_info.email).first()
            if exist_user:
                return ManagerCode.UserAlreadyExist
            pwd_hash, pwd_salt = await password_hashing(user_info.password)
            user = Users(
                name=user_info.name,
                email=user_info.email,
                role=user_info.role,
                team=user_info.team,
                pw_hash=pwd_hash,
                pw_salt=pwd_salt
            )
            print("-------", user)
            db_session.add(user)
            db_session.commit()
        logging.info(f"Success add User: username: {user_info.name}, email: {user_info.email}")
    except SQLAlchemyError as e:
        logging.error(f"Error while registering user: {e}")
        return ManagerCode.DataBaseError
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return ManagerCode.UnknownError
    return ManagerCode.Success
