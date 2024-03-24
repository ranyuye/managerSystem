from sqlalchemy import Column, Integer, String, Text, SmallInteger, DATETIME, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from app.utils.format_time import now


class DatabaseBaseModel:
    id = Column(Integer, primary_key=True, comment="auto pk_id")
    create_time = Column(DATETIME, default=now(), nullable=False, comment="create time")
    update_time = Column(DATETIME, default=now(), nullable=False, comment="update time")
    status = Column(SmallInteger, nullable=False, default=1, comment="status")


# 先定义基础的声明式基类
Base = declarative_base()


class Users(DatabaseBaseModel, Base):
    __tablename__ = 'users'
    name = Column(String, nullable=False, comment="user name")
    email = Column(String, nullable=False, comment="user email")
    role = Column(SmallInteger, nullable=False, comment="user role")
    team = Column(Integer, nullable=True, comment="user team")
    pw_hash = Column(Text, nullable=False, comment="password hash")
    pw_salt = Column(Text, nullable=False, comment="password salt")
    permission = Column(String, nullable=True, default="1", comment="user permission")
    dept_id = Column(Integer, nullable=True, comment="user dept id")


class Permissions(DatabaseBaseModel, Base):
    __tablename__ = 'permissions'
    pm_id = Column(Integer, nullable=False, comment="permission id")
    pm_name = Column(String, nullable=False, comment="permission name")
    pm_group = Column(Integer, nullable=False, comment="permission group")
    pm_desc = Column(String, nullable=True, comment="permission description")


class Dept(DatabaseBaseModel, Base):
    __tablename__ = 'dept'
    name = Column(String, nullable=False, comment="dept name")
    leader = Column(Integer, nullable=True, comment="dept leader id")


class DeptRelation(DatabaseBaseModel, Base):
    __tablename__ = 'dept_relation'
    child_dept_id = Column(Integer, ForeignKey("dept.id"), nullable=False, comment="dept id")
    parent_dept_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="user id")


