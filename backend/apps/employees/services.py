from sqlalchemy.orm import Query, Session

from apps.auth.models import User, UserRole
from apps.auth.services import get_password_hash
from apps.employees.models import Employee
from apps.employees.schemas import EmployeeCreate, EmployeeUpdate
from apps.organization.models import Department, JobTitle, PositionScope, Team


def validate_employee_assignment(
    db: Session,
    department_id: int,
    team_id: int,
    job_title_id: int,
):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise ValueError("Department not found")

    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise ValueError("Team not found")

    if team.department_id != department_id:  # type: ignore
        raise ValueError("Team does not belong to the given department")

    job_title = db.query(JobTitle).filter(JobTitle.id == job_title_id).first()
    if not job_title:
        raise ValueError("Job title not found")

    return department, team, job_title


def create_employee(db: Session, data: EmployeeCreate):
    existing_user = db.query(User).filter(User.matricule == data.matricule).first()
    if existing_user:
        raise ValueError("User with this matricule already exists")

    existing_email = db.query(Employee).filter(Employee.email == data.email).first()
    if existing_email:
        raise ValueError("Employee with this email already exists")

    validate_employee_assignment(
        db,
        data.department_id,
        data.team_id,
        data.job_title_id,
    )

    default_password = (data.first_name + data.last_name).lower() + "123"
    hashed_password = get_password_hash(default_password)

    user = User(
        matricule=data.matricule,
        hashed_password=hashed_password,
        role=UserRole.USER,
        is_active=True,
        first_login=True,
    )

    db.add(user)
    db.flush()

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


def get_visible_employees(db: Session, current_user: User) -> Query[Employee]:
    if current_user.role == UserRole.SUPERUSER:  # type: ignore
        return db.query(Employee)

    current_employee = get_employee_by_user_id(db, current_user.id)  # type: ignore
    job_title = current_employee.job_title
    scope = job_title.scope
    level = job_title.level

    query = db.query(Employee).join(JobTitle).filter(JobTitle.level < level)

    if scope == PositionScope.GLOBAL:
        return query

    if scope == PositionScope.DEPARTMENT:
        return query.filter(Employee.department_id == current_employee.department_id)

    if scope == PositionScope.TEAM:
        return query.filter(Employee.team_id == current_employee.team_id)

    return query.filter(Employee.id == current_employee.id)


def get_visible_employee_by_id(
    db: Session,
    employee_id: int,
    current_user: User,
) -> Employee:
    employee = (
        get_visible_employees(db, current_user)
        .filter(Employee.id == employee_id)
        .first()
    )
    if employee:
        return employee

    existing_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not existing_employee:
        raise ValueError("Employee not found")

    raise ValueError("You are not allowed to access this employee")


def list_employees(
    db: Session,
    current_user: User,
    department_id: int | None = None,
    team_id: int | None = None,
):
    query = get_visible_employees(db, current_user)

    if department_id is not None:
        query = query.filter(Employee.department_id == department_id)

    if team_id is not None:
        query = query.filter(Employee.team_id == team_id)

    return query.all()


def get_employee_by_id(db: Session, employee_id: int, current_user: User):
    return get_visible_employee_by_id(db, employee_id, current_user)


def get_employee_by_user_id(db: Session, user_id: int):
    employee = db.query(Employee).filter(Employee.user_id == user_id).first()
    if not employee:
        raise ValueError("Employee profile not found")
    return employee


def update_employee(
    db: Session,
    employee_id: int,
    current_user: User,
    data: EmployeeUpdate,
):
    employee = get_visible_employee_by_id(db, employee_id, current_user)
    update_data = data.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing_email = (
            db.query(Employee)
            .filter(
                Employee.email == update_data["email"],
                Employee.id != employee.id,
            )
            .first()
        )
        if existing_email:
            raise ValueError("Employee with this email already exists")

    target_department_id = update_data.get("department_id", employee.department_id)
    target_team_id = update_data.get("team_id", employee.team_id)
    target_job_title_id = update_data.get("job_title_id", employee.job_title_id)

    validate_employee_assignment(
        db,
        target_department_id,
        target_team_id,
        target_job_title_id,
    )

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee


def delete_employee(db: Session, employee_id: int, current_user: User):
    employee = get_visible_employee_by_id(db, employee_id, current_user)
    user = db.query(User).filter(User.id == employee.user_id).first()

    db.delete(employee)

    if user:
        db.delete(user)

    db.commit()

    return True
