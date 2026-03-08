from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from apps.auth.models import User

from db.session import get_db
from apps.auth.dependencies import require_superuser,require_active_user
from apps.employees.schemas import EmployeeCreate, EmployeeResponse,EmployeeListResponse
from apps.employees.services import (
    create_employee,
    list_employees,
    get_employee_by_user_id,
    get_employee_by_id,
    delete_employee,
    update_employee
)


router = APIRouter(prefix="/employees", tags=["Employees"])

