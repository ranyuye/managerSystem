from pydantic import BaseModel, Field


class DeptInfo(BaseModel):
    dept_name: str = Field(..., description="dept name")
    dept_leader: int = Field(..., description="dept leader")
    dept_parent: int = Field(None, description="dept parent")


class DeptUpdateInfo(DeptInfo):
    id: int  = Field(..., description="dept id")
    status: int = Field(..., description="dept status")
