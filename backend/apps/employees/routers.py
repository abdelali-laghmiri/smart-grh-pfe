from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from apps.auth.dependencies import get_current_user
from apps.auth.models import User
from apps.employees.schemas import (
    EmployeeCreate,
    EmployeeListResponse,
    EmployeeResponse,
    EmployeeUpdate,
)
from apps.employees.services import (
    create_employee,
    delete_employee,
    get_employee_by_id,
    list_employees,
    update_employee,
)
from apps.permissions.dependencies import require_permission
from db.session import get_db


router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/", response_model=EmployeeResponse)
def create_employee_endpoint(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("employees.create")),
):
    try:
        employee = create_employee(db, data)
        return employee
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[EmployeeListResponse])
def list_employees_endpoint(
    department_id: int | None = None,
    team_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    employees = list_employees(db, current_user, department_id, team_id)
    return employees


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee_endpoint(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        employee = get_employee_by_id(db, employee_id, current_user)
        return employee
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee_endpoint(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("employees.update")),
):
    try:
        employee = update_employee(db, employee_id, data)
        return employee
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{employee_id}")
def delete_employee_endpoint(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("employees.delete")),
):
    try:
        delete_employee(db, employee_id)
        return {"message": "Employee deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/me/profile", response_model=EmployeeResponse)
def my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from apps.employees.services import get_employee_by_user_id

    return get_employee_by_user_id(db, current_user.id)  # type: ignore
