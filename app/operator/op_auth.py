import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import jwt_info
from app.db_core.db_model import Users
from app.schema.auth_schema import UserInfo, LoginInfo
from app.schema.const_schema import ManagerResponse, ManagerCode
from app.schema.error_schema import DataNotExist, UserLoginError
from app.utils.jwt_auth import password_hashing, JwtAuth


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


async def login_user(login_info: LoginInfo, db_session: Session) -> (ManagerResponse, str):
    """
    login user
    :param login_info:
    :param db_session:
    :return:
    """
    response_status, token = ManagerCode.Success, ""
    try:
        with db_session as db_session:
            user = db_session.query(Users).filter(Users.email == login_info.email).first()
            if not user:
                raise DataNotExist
            if user.pw_hash != (await password_hashing(password=login_info.password, salt=user.pw_salt))[-1]:
                raise UserLoginError(message=f"The password for email '{user.email}' is wrong")
            token = JwtAuth(**jwt_info).create_access_token(data={"user_id": user.id})
    except SQLAlchemyError as e:
        logging.error(f"Error while longing user: {e}")
        response_status, token = ManagerCode.DataBaseError, ""
    except DataNotExist as e:
        logging.error(f"DataBase error: {e}")
        response_status, token = ManagerCode.UserNotExist, ""
    except UserLoginError as e:
        logging.error(f"User loging error: {e}")
        response_status, token = ManagerCode.UserLoginError, ""
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        response_status, token = ManagerCode.UnknownError, ""
    finally:
        return response_status, token

