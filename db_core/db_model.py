from sqlalchemy import Column, Integer, String, Text, SmallInteger, DATETIME
from db_connect import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, comment="auto pk_id")
    name = Column(String, nullable=False, comment="user name")
    email = Column(String, nullable=False, comment="user email")
    role = Column(SmallInteger, nullable=False, comment="user role")
    team = Column(Integer, nullable=True, comment="user team")
    pw_hash = Column(Text, nullable=False, comment="password hash")
    pw_salt = Column(Text, nullable=False, comment="password salt")
    create_time = Column(DATETIME, default=now(), nullable=False, comment="create time"))
