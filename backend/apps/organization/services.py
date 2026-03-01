from sqlalchemy.orm import Session
from apps.organization.models import JobTitle,Department
from apps.organization.schemas import JobTitleCreate

from apps.auth.models import User



#=============================job_title===============================

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
#=======================================Departement ================================================



def create_department(db: Session, name: str, description: str | None, manager_id: int | None):

    # 1️⃣ check uniqueness
    existing = db.query(Department).filter(Department.name == name).first()
    if existing:
        raise ValueError("Department already exists")

    # 2️⃣ check manager existence
    if manager_id:
        manager = db.query(User).filter(User.id == manager_id).first()
        if not manager:
            raise ValueError("Manager not found")

    # 3️⃣ create department
    department = Department(
        name=name,
        description=description,
        manager_id=manager_id,
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    return department

def list_departments(db: Session):
    return db.query(Department).all()

#========================= end ===================
def get_teams_by_department(db: Session, department_id: int):
    department = db.query(Department).filter(Department.id == department_id).first()

    if not department:
        raise ValueError("Department not found")

    return department.teams