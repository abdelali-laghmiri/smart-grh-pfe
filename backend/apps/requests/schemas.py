from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict

# =====================================================
# Request Schemas
# Pydantic models for request types, workflow steps,
# employee requests, and approval actions.
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


# =====================================================
# Request Type Schemas
# Defines payloads for request type configuration.
# =====================================================


class RequestTypeBase(BaseModel):
    """Shared fields used by request type payloads."""

    name: str
    description: str | None = None


class RequestTypeCreate(RequestTypeBase):
    """Payload used to create a new request type."""

    pass


class RequestTypeResponse(RequestTypeBase):
    """Serialized representation of a request type."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Approval Step Schemas
# Defines payloads for workflow step configuration.
# =====================================================


class ApprovalStepBase(BaseModel):
    """Shared fields used by approval step payloads."""

    request_type_id: int
    step_order: int
    job_title_id: int


class ApprovalStepCreate(ApprovalStepBase):
    """Payload used to create a workflow approval step."""

    pass


class ApprovalStepResponse(ApprovalStepBase):
    """Serialized representation of a workflow approval step."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Request Schemas
# Defines payloads for employee request creation and reads.
# =====================================================


class RequestCreate(BaseModel):
    """Payload used when an employee creates a request."""

    request_type_id: int
    extra_data: dict[str, Any] | None = None


class RequestResponse(BaseModel):
    """Serialized representation of a request."""

    id: int
    employee_id: int
    request_type_id: int
    status: RequestStatus
    current_step: int | None
    extra_data: dict[str, Any] | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Approval Schemas
# Defines payloads for approval inbox responses and actions.
# =====================================================


class ApprovalResponse(BaseModel):
    """Serialized representation of a generated approval step."""

    id: int
    request_id: int
    approver_user_id: int
    step_order: int
    status: ApprovalStatus
    approved_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ApprovalAction(BaseModel):
    """Optional payload sent when approving or rejecting a request."""

    comment: str | None = None


class ActionResponse(BaseModel):
    """Simple response payload returned by workflow actions."""

    message: str
