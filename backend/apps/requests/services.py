from sqlalchemy.orm import Session
from datetime import datetime

from apps.requests.models import (
    Request,
    RequestApproval,
    ApprovalStep,
    RequestStatus,
    ApprovalStatus
)

from apps.employees.models import Employee
from apps.employees.services import get_employee_by_user_id
from apps.organization.models import JobTitle, PositionScope
from apps.auth.models import User

# =====================================================
# Request Services
# Handles workflow generation and approval progression.
# =====================================================


# =========================
# FIND APPROVER
# =========================

def find_approver_by_job_title(
    db: Session,
    employee: Employee,
    job_title: JobTitle
):
    """Resolve the approver user according to the job title scope."""

    scope = job_title.scope

    query = db.query(Employee).filter(
        Employee.job_title_id == job_title.id
    )

    if scope == PositionScope.TEAM:
        query = query.filter(
            Employee.team_id == employee.team_id
        )

    elif scope == PositionScope.DEPARTMENT:
        query = query.filter(
            Employee.department_id == employee.department_id
        )

    approver = query.first()

    if not approver:
        raise ValueError("Approver not found")

    return approver.user_id


# =========================
# CREATE REQUEST
# =========================

def create_request(
    db: Session,
    current_user: User,
    request_type_id: int,
    extra_data: dict | None = None
):
    """Create a request and generate its approval records."""

    employee = get_employee_by_user_id(db, current_user.id)

    if not employee:
        raise ValueError("Employee profile not found")

    steps = (
        db.query(ApprovalStep)
        .filter(ApprovalStep.request_type_id == request_type_id)
        .order_by(ApprovalStep.step_order)
        .all()
    )

    if not steps:
        raise ValueError("No approval workflow defined")

    request = Request(
        employee_id=employee.id,
        request_type_id=request_type_id,
        status=RequestStatus.PENDING,
        current_step=1,
        extra_data=extra_data
    )

    db.add(request)
    db.flush()

    for step in steps:
        # Each workflow step is materialized so the assigned approver is fixed
        # at request creation time.

        approver_user_id = find_approver_by_job_title(
            db,
            employee,
            step.job_title
        )

        approval = RequestApproval(
            request_id=request.id,
            step_order=step.step_order,
            approver_user_id=approver_user_id,
            status=ApprovalStatus.PENDING
        )

        db.add(approval)

    db.commit()
    db.refresh(request)

    return request


# =========================
# MY REQUESTS
# =========================

def get_my_requests(
    db: Session,
    current_user: User
):
    """Return the requests created by the current user."""

    employee = get_employee_by_user_id(db, current_user.id)

    return db.query(Request).filter(
        Request.employee_id == employee.id
    ).all()


# =========================
# MY APPROVALS
# =========================

def get_my_approvals(
    db: Session,
    current_user: User
):
    """Return pending approval tasks assigned to the current user."""

    return db.query(RequestApproval).filter(
        RequestApproval.approver_user_id == current_user.id,
        RequestApproval.status == ApprovalStatus.PENDING
    ).all()


# =========================
# APPROVE REQUEST
# =========================

def approve_request(
    db: Session,
    approval_id: int,
    current_user: User
):
    """Approve the current workflow step and advance the request."""

    approval = db.query(RequestApproval).filter(
        RequestApproval.id == approval_id
    ).first()

    if not approval:
        raise ValueError("Approval not found")

    if approval.approver_user_id != current_user.id:
        raise ValueError("Not allowed")

    approval.status = ApprovalStatus.APPROVED
    approval.approved_at = datetime.utcnow()

    request = approval.request

    # Move the request to the next workflow step, or finalize it when the
    # current approval completes the workflow.
    next_step = request.current_step + 1

    next_approval = db.query(RequestApproval).filter(
        RequestApproval.request_id == request.id,
        RequestApproval.step_order == next_step
    ).first()

    if next_approval:
        request.current_step = next_step
    else:
        request.status = RequestStatus.APPROVED
        request.current_step = None

    db.commit()

    return True


# =========================
# REJECT REQUEST
# =========================

def reject_request(
    db: Session,
    approval_id: int,
    current_user: User
):
    """Reject the current workflow step and close the request."""

    approval = db.query(RequestApproval).filter(
        RequestApproval.id == approval_id
    ).first()

    if not approval:
        raise ValueError("Approval not found")

    if approval.approver_user_id != current_user.id:
        raise ValueError("Not allowed")

    approval.status = ApprovalStatus.REJECTED
    approval.approved_at = datetime.utcnow()

    request = approval.request

    request.status = RequestStatus.REJECTED
    request.current_step = None

    db.commit()

    return True
