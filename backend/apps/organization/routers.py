from fastapi import APIRouter
from apps.organization.schemas import JobTitleCreate,JobTitleResponse
from datetime import datetime

router =APIRouter(prefix="/organization",tags=["organization"])




@router.post("/test-job-title", response_model=JobTitleResponse)
def test_job_title(data: JobTitleCreate):
    return {
        "id": 1,
        "title": data.title,
        "scope": data.scope,
        "level": data.level,
        "description": data.description,
        "monthly_leave_accrual": data.monthly_leave_accrual,
        "created_at": datetime.utcnow(),
    }