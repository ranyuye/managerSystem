from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    name: str = Field(..., description="user name")
    email: str = Field(..., description="user email")
    password: str = Field(..., description="user password")
    role: int = Field(..., description="user role")
    team: int = Field(..., description="user team")


class LoginInfo(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., description="user password")
