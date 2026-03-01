from pydantic import BaseModel
from datetime import datetime

from apps.organization.models import PositionScope

#=============== 🏢 1️⃣ JobTitle Schemas =================#

class JobTitleBase(BaseModel):
    title: str
    scope: PositionScope
    level: int
    description: str | None = None
    monthly_leave_accrual: float = 0.0


class JobTitleCreate(JobTitleBase):
    pass


class JobTitleResponse(JobTitleBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
#=============== end of JobTitle Schemas =================#
#=============== 👥 2️⃣ Department Schemas =================#
class DepartmentBase(BaseModel):
    name: str
    description: str | None = None
    manager_id: int | None = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
#=============== end of JobTitle Schemas ===================#
#=============== 👥 3️⃣ Team Schemas ===================#
class TeamBase(BaseModel):
    name: str
    department_id: int
    team_leader_id: int | None = None


class TeamCreate(TeamBase):
    pass


class TeamResponse(TeamBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
#=============== end of Team Schemas ===================#