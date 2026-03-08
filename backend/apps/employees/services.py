from sqlalchemy.orm import Session
from apps.auth.models import User, UserRole
from apps.auth.services import get_password_hash
from apps.organization.models import Department, Team, JobTitle, PositionScope
from apps.employees.models import Employee
from apps.employees.schemas import EmployeeCreate,EmployeeUpdate

#=========
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
#========
def get_visible_employees(db: Session, current_user ):

    if current_user.role == UserRole.SUPERUSER:
        return db.query(Employee).all()

    current_employee = get_employee_by_user_id(db, current_user.id)

    job_title = current_employee.job_title
    scope = job_title.scope
    level = job_title.level

    query = db.query(Employee).join(JobTitle)

    query = query.filter(JobTitle.level < level)

    if scope == PositionScope.GLOBAL:
        return query.all()

    if scope == PositionScope.DEPARTMENT:
        query = query.filter(
            Employee.department_id == current_employee.department_id
        )

    if scope == PositionScope.TEAM:
        query = query.filter(
            Employee.team_id == current_employee.team_id
        )

    if scope == PositionScope.NONE:
        return [current_employee]

    return query.all()
#=========
def list_employees(db: Session, current_user: User):
    employees = get_visible_employees (db ,current_user)
    return employees
#=========
def get_employee_by_id (db : Session ,employee_id : int, current_user : User):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise ValueError("Employee not found ")
    visible_emplouiyees = get_visible_employees(db,current_user)
    
    if employee not in visible_emplouiyees : 
        raise ValueError("You are not allowed to view this employee")

    return employee
#=========
def get_employee_by_user_id(db: Session, user_id: int):
    employee = db.query(Employee).filter(Employee.user_id == user_id).first()
    if not employee:
        raise ValueError("Employee profile not found")
    return employee
#=========
def update_employee(
    db: Session,
    employee_id: int,
    data: EmployeeUpdate,
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise ValueError("Employee not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee
#=========
def delete_employee(db: Session, employee_id: int):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise ValueError("Employee not found")

    user = db.query(User).filter(User.id == employee.user_id).first()

    db.delete(employee)

    if user:
        db.delete(user)

    db.commit()

    return True
#=========




