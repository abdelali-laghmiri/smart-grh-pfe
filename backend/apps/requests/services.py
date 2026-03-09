from datetime import datetime

from sqlalchemy.orm import Session

from apps.auth.models import User
from apps.employees.models import Employee
from apps.employees.services import get_employee_by_user_id
from apps.organization.models import JobTitle, PositionScope
from apps.requests.models import (
    ApprovalStatus,
    ApprovalStep,
    Request,
    RequestApproval,
    RequestStatus,
    RequestType,
)

# =====================================================
# Request Services
# Handles request type configuration, workflow setup,
# request creation, and approval progression.
# =====================================================


# =====================================================
# Request Type Service
# Handles creation and retrieval of request types.
# =====================================================


def create_request_type(
    db: Session,
    name: str,
    description: str | None = None,
) -> RequestType:
    """Create a new request type after validating uniqueness."""

    existing = db.query(RequestType.id).filter(RequestType.name == name).first()
    if existing:
        raise ValueError("Request type already exists")

    request_type = RequestType(
        name=name,
        description=description,
    )

    db.add(request_type)
    db.commit()
    db.refresh(request_type)
    return request_type


def list_request_types(db: Session):
    """Return all request types ordered by their creation identifier."""

    return db.query(RequestType).order_by(RequestType.id).all()


# =====================================================
# Approval Step Service
# Handles workflow step creation and retrieval.
# =====================================================


def create_approval_step(
    db: Session,
    request_type_id: int,
    step_order: int,
    job_title_id: int,
) -> ApprovalStep:
    """Create a workflow step for a request type."""

    request_type = db.query(RequestType.id).filter(RequestType.id == request_type_id).first()
    if not request_type:
        raise ValueError("Request type not found")

    job_title = db.query(JobTitle.id).filter(JobTitle.id == job_title_id).first()
    if not job_title:
        raise ValueError("Job title not found")

    if step_order <= 0:
        raise ValueError("Step order must be greater than 0")

    existing = (
        db.query(ApprovalStep.id)
        .filter(
            ApprovalStep.request_type_id == request_type_id,
            ApprovalStep.step_order == step_order,
        )
        .first()
    )
    if existing:
        raise ValueError("A workflow step with this order already exists")

    step = ApprovalStep(
        request_type_id=request_type_id,
        step_order=step_order,
        job_title_id=job_title_id,
    )

    db.add(step)
    db.commit()
    db.refresh(step)
    return step


def get_request_type_steps(db: Session, request_type_id: int):
    """Return workflow steps for a request type ordered by step number."""

    request_type = db.query(RequestType.id).filter(RequestType.id == request_type_id).first()
    if not request_type:
        raise ValueError("Request type not found")

    return (
        db.query(ApprovalStep)
        .filter(ApprovalStep.request_type_id == request_type_id)
        .order_by(ApprovalStep.step_order)
        .all()
    )


# =====================================================
# Request Workflow Helpers
# Shared helper functions used by request actions.
# =====================================================


def find_approver_by_job_title(
    db: Session,
    employee: Employee,
    job_title: JobTitle,
):
    """Resolve the approver user according to the job title scope."""

    scope = job_title.scope

    query = db.query(Employee).filter(
        Employee.job_title_id == job_title.id
    )

    if scope == PositionScope.TEAM: # type: ignore
        query = query.filter(
            Employee.team_id == employee.team_id
        )

    elif scope == PositionScope.DEPARTMENT: # type: ignore
        query = query.filter(
            Employee.department_id == employee.department_id
        )

    approver = query.first()

    if not approver:
        raise ValueError("Approver not found")

    return approver.user_id


def get_pending_approval_for_request(
    db: Session,
    request_id: int,
    current_user: User,
) -> RequestApproval:
    """Return the current pending approval assigned to the current user."""

    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise ValueError("Request not found")

    if request.status != RequestStatus.PENDING or request.current_step is None: # type: ignore
        raise ValueError("Request is not awaiting approval")

    approval = (
        db.query(RequestApproval)
        .filter(
            RequestApproval.request_id == request.id,
            RequestApproval.step_order == request.current_step,
            RequestApproval.approver_user_id == current_user.id,
            RequestApproval.status == ApprovalStatus.PENDING,
        )
        .first()
    )

    if not approval:
        raise ValueError("Approval not found")

    return approval


# =====================================================
# Request Service
# Handles creation and retrieval of employee requests.
# =====================================================


def create_request(
    db: Session,
    current_user: User,
    request_type_id: int,
    extra_data: dict | None = None,
):
    """Create a request and generate its approval records."""

    employee = get_employee_by_user_id(db, current_user.id) # type: ignore

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
        extra_data=extra_data,
    )

    db.add(request)
    db.flush()

    for step in steps:
        # Each workflow step is materialized so the assigned approver is fixed
        # at request creation time.
        approver_user_id = find_approver_by_job_title(
            db,
            employee,
            step.job_title,
        )

        approval = RequestApproval(
            request_id=request.id,
            step_order=step.step_order,
            approver_user_id=approver_user_id,
            status=ApprovalStatus.PENDING,
        )

        db.add(approval)

    db.commit()
    db.refresh(request)
    return request


def get_my_requests(
    db: Session,
    current_user: User,
):
    """Return the requests created by the current user."""

    employee = get_employee_by_user_id(db, current_user.id) # type: ignore

    return (
        db.query(Request)
        .filter(Request.employee_id == employee.id)
        .order_by(Request.id)
        .all()
    )


def get_my_approvals(
    db: Session,
    current_user: User,
):
    """Return pending approval tasks assigned to the current user."""

    return (
        db.query(RequestApproval)
        .filter(
            RequestApproval.approver_user_id == current_user.id,
            RequestApproval.status == ApprovalStatus.PENDING,
        )
        .order_by(RequestApproval.request_id, RequestApproval.step_order)
        .all()
    )


# =====================================================
# Approval Action Service
# Handles approve and reject actions on workflow steps.
# =====================================================


def approve_request(
    db: Session,
    request_id: int,
    current_user: User,
    comment: str | None = None,
):
    """Approve the current workflow step and advance the request."""

    # Approval comments are accepted by the API contract, but the current
    # data model does not persist them.
    _ = comment

    approval = get_pending_approval_for_request(db, request_id, current_user)

    approval.status = ApprovalStatus.APPROVED # type: ignore
    approval.approved_at = datetime.utcnow() # type: ignore

    request = approval.request

    # Move the request to the next workflow step, or finalize it when the
    # current approval completes the workflow.
    next_step = request.current_step + 1

    next_approval = db.query(RequestApproval).filter(
        RequestApproval.request_id == request.id,
        RequestApproval.step_order == next_step,
    ).first()

    if next_approval:
        request.current_step = next_step
    else:
        request.status = RequestStatus.APPROVED
        request.current_step = None

    db.commit()
    return True


def reject_request(
    db: Session,
    request_id: int,
    current_user: User,
    comment: str | None = None,
):
    """Reject the current workflow step and close the request."""

    # Approval comments are accepted by the API contract, but the current
    # data model does not persist them.
    _ = comment

    approval = get_pending_approval_for_request(db, request_id, current_user)

    approval.status = ApprovalStatus.REJECTED # type: ignore
    approval.approved_at = datetime.utcnow() # type: ignore

    request = approval.request
    request.status = RequestStatus.REJECTED
    request.current_step = None

    db.commit()
    return True
