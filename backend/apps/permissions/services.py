from sqlalchemy.orm import Session

from apps.auth.models import User
from apps.employees.models import Employee
from apps.permissions.models import Permission, JobTitlePermission


def user_has_permission(
    db: Session,
    user: User,
    permission_name: str
) -> bool:

    employee = db.query(Employee).filter(
        Employee.user_id == user.id
    ).first()

    if not employee:
        return False

    permission = (
        db.query(Permission)
        .join(JobTitlePermission)
        .filter(
            JobTitlePermission.job_title_id == employee.job_title_id,
            Permission.name == permission_name
        )
        .first()
    )

    return permission is not None