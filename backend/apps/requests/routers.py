from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from apps.auth.dependencies import get_current_user
from apps.permissions.dependencies import require_permission

from . import schemas
from . import services

# =====================================================
# Request Router
# Exposes employee request and approval workflow endpoints.
# =====================================================


router = APIRouter(
    prefix="/requests",
    tags=["Requests"]
)

@router.post("/", response_model=schemas.RequestResponse)
def create_request(
    data: schemas.RequestCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Create a new request for the authenticated user."""
    return services.create_request(db, current_user, data) # type: ignore

@router.get("/my", response_model=list[schemas.RequestResponse])
def get_my_requests(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Return requests created by the authenticated user."""
    return services.get_my_requests(db, current_user)

@router.get("/approvals", response_model=list[schemas.ApprovalResponse])
def get_my_approvals(
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("approver"))
):
    """Return approval tasks assigned to the authenticated approver."""
    return services.get_my_approvals(db, current_user)

@router.post("/{request_id}/approve")
def approve_request(
    request_id: int,
    data: schemas.ApprovalAction,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Approve a request step assigned to the authenticated user."""
    return services.approve_request(db, current_user, request_id, data) # type: ignore


@router.post("/{request_id}/reject")
def reject_request(
    request_id: int,
    data: schemas.ApprovalAction,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Reject a request step assigned to the authenticated user."""
    return services.reject_request(db, current_user, request_id, data) # type: ignore
