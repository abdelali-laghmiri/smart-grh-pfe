from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from apps.auth.dependencies import require_superuser
from apps.employees.schemas import EmployeeCreate, EmployeeResponse
from apps.employees.services import create_employee


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