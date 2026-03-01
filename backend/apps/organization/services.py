from sqlalchemy.orm import Session
from apps.organization.models import JobTitle
from apps.organization.schemas import JobTitleCreate



#============================================================

def create_job_title(db : Session , data : JobTitleCreate) -> JobTitle : 
    existing = db.query(JobTitle).filter(JobTitle.title == data.title).first()
    if existing : 
        raise ValueError("Job title already exists")
    if data.level <= 0 : 
        raise ValueError("Level must be greater than 0")
    job_title = JobTitle(
        title=data.title,
        scope=data.scope,
        level=data.level,
        description=data.description,
        monthly_leave_accrual=data.monthly_leave_accrual,
    )
    db.add(job_title)
    db.commit()
    db.refresh(job_title)
    return job_title
def delete_job_title(db: Session, job_title_id: int):
    job_title = db.query(JobTitle).filter(JobTitle.id == job_title_id).first()

    if not job_title:
        raise ValueError("Job title not found")

    # TODO: prevent deletion if linked to employees (after employees app is created)

    db.delete(job_title)
    db.commit()

    return True
#============================================================