from pydantic import BaseModel, EmailStr
from datetime import date


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