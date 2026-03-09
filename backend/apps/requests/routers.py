from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.auth.dependencies import get_current_user, require_active_user, require_superuser
from apps.auth.models import User
from db.session import get_db

from . import schemas
from . import services

# =====================================================
# Request Router
# Exposes endpoints for request types, workflow steps,
# employee requests, and approval actions.
# =====================================================


router = APIRouter(
    prefix="/requests",
    tags=["Requests"],
)


# =====================================================
# Request Type Routes
# Handles request type configuration.
# =====================================================


@router.post("/types", response_model=schemas.RequestTypeResponse)
def create_request_type_endpoint(
    data: schemas.RequestTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_superuser),
):
    """Create a request type. Restricted to superusers."""

    try:
        return services.create_request_type(
            db,
            name=data.name,
            description=data.description,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/types", response_model=list[schemas.RequestTypeResponse])
def list_request_types_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
):
    """List all available request types."""

    return services.list_request_types(db)


# =====================================================
# Workflow Step Routes
# Handles approval workflow step configuration.
# =====================================================


@router.post("/steps", response_model=schemas.ApprovalStepResponse)
def create_approval_step_endpoint(
    data: schemas.ApprovalStepCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_superuser),
):
    """Create a workflow step for a request type. Restricted to superusers."""

    try:
        return services.create_approval_step(
            db,
            request_type_id=data.request_type_id,
            step_order=data.step_order,
            job_title_id=data.job_title_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/types/{type_id}/steps", response_model=list[schemas.ApprovalStepResponse])
def get_request_type_steps_endpoint(
    type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
):
    """Return workflow steps for the given request type ordered by step order."""

    try:
        return services.get_request_type_steps(db, type_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# Request Routes
# Handles employee request submission and retrieval.
# =====================================================


@router.post("/", response_model=schemas.RequestResponse)
def create_request_endpoint(
    data: schemas.RequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new request for the authenticated user."""

    try:
        return services.create_request(
            db,
            current_user,
            request_type_id=data.request_type_id,
            extra_data=data.extra_data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/my", response_model=list[schemas.RequestResponse])
def get_my_requests_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return requests created by the authenticated user."""

    return services.get_my_requests(db, current_user)


@router.get("/approvals", response_model=list[schemas.ApprovalResponse])
def get_my_approvals_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return pending approval steps assigned to the authenticated user."""

    return services.get_my_approvals(db, current_user)


# =====================================================
# Approval Action Routes
# Handles approve and reject actions on requests.
# =====================================================


@router.post("/{request_id}/approve", response_model=schemas.ActionResponse)
def approve_request_endpoint(
    request_id: int,
    data: schemas.ApprovalAction,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Approve the current request step assigned to the authenticated user."""

    try:
        services.approve_request(db, request_id, current_user, data.comment)
        return {"message": "Request approved successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/{request_id}/reject", response_model=schemas.ActionResponse)
def reject_request_endpoint(
    request_id: int,
    data: schemas.ApprovalAction,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Reject the current request step assigned to the authenticated user."""

    try:
        services.reject_request(db, request_id, current_user, data.comment)
        return {"message": "Request rejected successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
