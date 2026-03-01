from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from apps.organization.models import JobTitle

from db.session import get_db
from apps.organization.schemas import JobTitleCreate, JobTitleResponse
from apps.organization.services import create_job_title

from apps.auth.dependencies import require_superuser, require_active_user


router = APIRouter(prefix="/organization", tags=["Organization"])

  
#=================== job-titles routers ==================================#
@router.post("/job-titels",response_model=JobTitleResponse)
def create_job_title_endpoint(
    data: JobTitleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_superuser),
):
    try:
        job_title = create_job_title(db, data)
        return job_title
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
@router.get("/job-titles", response_model=list[JobTitleResponse])
def list_job_titles(
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user),
):
    return db.query(JobTitle).all()
#=================== end  job-titles routers =============================#