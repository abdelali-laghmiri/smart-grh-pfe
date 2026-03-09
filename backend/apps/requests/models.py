from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from db.base import Base


# =========================
# ENUMS
# =========================

class RequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


# =========================
# REQUEST TYPES
# =========================

class RequestType(Base):
    __tablename__ = "request_types"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, nullable=False)

    description = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    approval_steps = relationship(
        "ApprovalStep",
        back_populates="request_type",
        cascade="all, delete"
    )

    requests = relationship("Request", back_populates="request_type")


# =========================
# APPROVAL WORKFLOW
# =========================

class ApprovalStep(Base):
    __tablename__ = "approval_steps"

    id = Column(Integer, primary_key=True, index=True)

    request_type_id = Column(Integer, ForeignKey("request_types.id"), nullable=False)

    step_order = Column(Integer, nullable=False)

    job_title_id = Column(Integer, ForeignKey("job_titles.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    request_type = relationship(
        "RequestType",
        back_populates="approval_steps"
    )

    job_title = relationship("JobTitle")

    __table_args__ = (
        UniqueConstraint("request_type_id", "step_order", name="uix_request_step_order"),
    )


# =========================
# REQUEST
# =========================

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    request_type_id = Column(Integer, ForeignKey("request_types.id"), nullable=False)

    status = Column(
        Enum(RequestStatus),
        default=RequestStatus.PENDING,
        nullable=False
    )

    current_step = Column(Integer, nullable=True)

    extra_data = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employee = relationship("Employee")

    request_type = relationship("RequestType", back_populates="requests")

    approvals = relationship(
        "RequestApproval",
        back_populates="request",
        cascade="all, delete"
    )


# =========================
# REQUEST APPROVAL HISTORY
# =========================

class RequestApproval(Base):
    __tablename__ = "request_approvals"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)

    step_order = Column(Integer, nullable=False)

    approver_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    status = Column(
        Enum(ApprovalStatus),
        default=ApprovalStatus.PENDING,
        nullable=False
    )

    approved_at = Column(DateTime(timezone=True), nullable=True)

    request = relationship(
        "Request",
        back_populates="approvals"
    )

    approver = relationship("User")
