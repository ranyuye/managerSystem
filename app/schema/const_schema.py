from typing import Union, Dict

from pydantic import BaseModel


class ManagerResponse(BaseModel):
    code: int
    msg: str
    data: Union[Dict, None] = None


class CodeWithMsg:
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg

    def __iter__(self):
        return iter([self.code, self.msg])


class ManagerCode:
    Success = CodeWithMsg(10000, "success")
    UnknownError = CodeWithMsg(10001, "error")
    DataBaseError = CodeWithMsg(10002, "database error")
    UserAlreadyExist = CodeWithMsg(20001, "user already exist")
    UserNotExist = CodeWithMsg(20002, "user not exist")
    UserLoginError = CodeWithMsg(20003, "user email or password is error")
    DeptNotExist = CodeWithMsg(30001, "dept not exist")