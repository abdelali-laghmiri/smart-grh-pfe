from sqlalchemy.orm import Session
from apps.auth.models import User, UserRole
from apps.auth.services import get_password_hash
from apps.organization.models import Department, Team, JobTitle
from apps.employees.models import Employee
from apps.employees.schemas import EmployeeCreate


def create_employee(db: Session, data: EmployeeCreate):

    # 1️⃣ Check matricule uniqueness
    existing_user = db.query(User).filter(User.matricule == data.matricule).first()
    if existing_user:
        raise ValueError("User with this matricule already exists")

    # 2️⃣ Check email uniqueness
    existing_email = db.query(Employee).filter(Employee.email == data.email).first()
    if existing_email:
        raise ValueError("Employee with this email already exists")

    # 3️⃣ Check department exists
    department = db.query(Department).filter(Department.id == data.department_id).first()
    if not department:
        raise ValueError("Department not found")

    # 4️⃣ Check team exists
    team = db.query(Team).filter(Team.id == data.team_id).first()
    if not team:
        raise ValueError("Team not found")

    # 5️⃣ Ensure team belongs to department
    if team.department_id != data.department_id: # type: ignore
        raise ValueError("Team does not belong to the given department")

    # 6️⃣ Check job title exists
    job_title = db.query(JobTitle).filter(JobTitle.id == data.job_title_id).first()
    if not job_title:
        raise ValueError("Job title not found")

    # 🔐 Create default password
    default_password = (data.first_name + data.last_name).lower() + "123"
    hashed_password = get_password_hash(default_password)

    # 7️⃣ Create User (no commit yet)
    user = User(
        matricule=data.matricule,
        hashed_password=hashed_password,
        role=UserRole.USER,
        is_active=True,
        first_login=True,
    )

    db.add(user)
    db.flush()  
    # 8️⃣ Create Employee
    employee = Employee(
        user_id=user.id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        phone=data.phone,
        hire_date=data.hire_date,
        department_id=data.department_id,
        team_id=data.team_id,
        job_title_id=data.job_title_id,
        current_leave_balance=0,
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee