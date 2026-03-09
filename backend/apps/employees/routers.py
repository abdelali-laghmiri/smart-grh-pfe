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
    get_employee_by_user_id,
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
        return create_employee(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me/profile", response_model=EmployeeResponse)
def my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_employee_by_user_id(db, current_user.id)  # type: ignore[arg-type]


@router.get("/", response_model=list[EmployeeListResponse])
def list_employees_endpoint(
    department_id: int | None = None,
    team_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return list_employees(
            db,
            current_user,
            department_id=department_id,
            team_id=team_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee_endpoint(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_employee_by_id(db, employee_id, current_user)
    except ValueError as e:
        detail = str(e)
        status_code = 403 if "not allowed" in detail.lower() else 404
        raise HTTPException(status_code=status_code, detail=detail)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee_endpoint(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("employees.update")),
):
    try:
        return update_employee(db, employee_id, current_user, data)
    except ValueError as e:
        detail = str(e)
        status_code = 403 if "not allowed" in detail.lower() else 400
        raise HTTPException(status_code=status_code, detail=detail)


@router.delete("/{employee_id}")
def delete_employee_endpoint(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("employees.delete")),
):
    try:
        delete_employee(db, employee_id, current_user)
        return {"message": "Employee deleted successfully"}
    except ValueError as e:
        detail = str(e)
        status_code = 403 if "not allowed" in detail.lower() else 404
        raise HTTPException(status_code=status_code, detail=detail)
