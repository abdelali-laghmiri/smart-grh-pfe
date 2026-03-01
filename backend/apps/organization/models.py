from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from apps.auth.models import User
from db.base import Base

class PositionScope(str,enum.Enum):
    TEAM = "TEAM"
    DEPARTMENT = "DEPARTMENT"
    GLOBAL = "GLOBAL"

class JobTitel(Base):
    __tablename__ = "job_titel"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String, unique=True,nullable=False)
    scope = Column(Enum(PositionScope),nullable=False)
    description = Column(String,nullable=True)
    monthly_leave_accrual = Column(Integer,nullable=True,default=0)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    manager = relationship(
                            "User",
                            back_populates="managed_departments",
                            foreign_keys=[manager_id]
                            )
    teams = relationship("Team", back_populates="department", cascade="all, delete")

class Team(Base):
    __tablename__  = "teams"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)

    department_id = Column(Integer, ForeignKey("departments.id"),nullable=False)
    team_leader_id = Column(Integer,ForeignKey("users.id"),nullable=True)

    department = relationship("Department", back_populates="teams")
    team_leader = relationship(
    "User",
    back_populates="led_teams",
    foreign_keys=[team_leader_id]
)

    __table_args__ = (
        UniqueConstraint("department_id", "name", name="uix_department_team"),
    )