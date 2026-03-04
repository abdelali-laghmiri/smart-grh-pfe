from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from apps.auth.models import User

from db.session import get_db
from apps.auth.dependencies import require_superuser,require_active_user
from apps.employees.schemas import EmployeeCreate, EmployeeResponse,EmployeeListResponse
from apps.employees.services import create_employee,list_employees,get_employee_by_user_id,get_employee_by_id


router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("", response_model=EmployeeResponse)
def create_employee_endpoint(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_superuser),
):
    try:
        return create_employee(db, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    




@router.get("/me", response_model=EmployeeResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
):
    try:
        return get_employee_by_user_id(db, current_user.id) # type: ignore
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
@router.get("", response_model=list[EmployeeListResponse])
def list_employees_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
):
    return list_employees(db, current_user)
@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee_by_id_endpoint(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
):
    try:
        return get_employee_by_id(db, employee_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )