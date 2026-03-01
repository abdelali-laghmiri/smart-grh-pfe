from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
import enum

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

