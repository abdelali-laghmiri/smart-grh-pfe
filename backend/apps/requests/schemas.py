from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

# =====================================================
# Request Schemas
# Pydantic models for request and approval payloads.
# =====================================================


class RequestStatus(str, Enum):
    """Serialized status of a request."""

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ApprovalStatus(str, Enum):
    """Serialized status of an approval step."""

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


# =========================
# REQUEST CREATE
# =========================

class RequestCreate(BaseModel):
    """Payload used when an employee creates a request."""

    request_type_id: int
    extra_data: Optional[Dict] = None


# =========================
# REQUEST RESPONSE
# =========================

class RequestResponse(BaseModel):
    """Serialized representation of a request."""

    id: int
    employee_id: int
    request_type_id: int
    status: RequestStatus
    current_step: int
    extra_data: Optional[Dict]
    created_at: datetime

    class Config:
        from_attributes  = True


# =========================
# APPROVAL RESPONSE
# =========================

class ApprovalResponse(BaseModel):
    """Serialized representation of a generated approval step."""

    id: int
    request_id: int
    approver_user_id: int
    step_order: int
    status: ApprovalStatus

    class Config:
        from_attributes  = True


# =========================
# APPROVE / REJECT
# =========================

class ApprovalAction(BaseModel):
    """Optional payload sent when approving or rejecting a request."""

    comment: Optional[str] = None



