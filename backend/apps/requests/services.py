from sqlalchemy.orm import Session
from datetime import datetime

from apps.requests.models import (
    Request,
    RequestApproval,
    ApprovalStep,
    RequestStatus,
    ApprovalStatus
)

from apps.employees.services import get_employee_by_user_id
from apps.auth.models import User


def create_request(
    db: Session,
    current_user: User ,
    request_type_id: int
):

    # 1️⃣ get employee profile
    employee = get_employee_by_user_id(db, current_user.id) # type: ignore

    if not employee:
        raise ValueError("Employee profile not found")

    # 2️⃣ get approval workflow steps
    steps = (
        db.query(ApprovalStep)
        .filter(ApprovalStep.request_type_id == request_type_id)
        .order_by(ApprovalStep.step_order)
        .all()
    )

    if not steps:
        raise ValueError("No approval workflow defined for this request type")

    # 3️⃣ create request
    request = Request(
        employee_id=employee.id,
        request_type_id=request_type_id,
        status=RequestStatus.PENDING,
        current_step=1
    )

    db.add(request)

    
    db.flush()

    # 4️⃣ create approval records
    for step in steps:

        approval = RequestApproval(
            request_id=request.id,
            step_order=step.step_order,
            approver_user_id=None, 
            status=ApprovalStatus.PENDING
        )

        db.add(approval)

    db.commit()
    db.refresh(request)

    return request