from pydantic import BaseModel, EmailStr
from datetime import date
from apps.employees.models import EmploymentStatus

class EmployeeCreate(BaseModel):
    matricule: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    hire_date: date
    department_id: int
    team_id: int
    job_title_id: int





class EmployeeResponse(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
    hire_date: date
    department_id: int
    team_id: int
    job_title_id: int
    current_leave_balance: int
    employment_status: EmploymentStatus

    class Config:
        from_attributes = True

class EmployeeListResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    department_id: int
    team_id: int
    job_title_id: int
    employment_status: EmploymentStatus

    class Config:
        from_attributes = True
class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    hire_date: date | None = None
    department_id: int | None = None
    team_id: int | None = None
    job_title_id: int | None = None
    employment_status: EmploymentStatus | None = None