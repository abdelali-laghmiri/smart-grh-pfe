"""Database bootstrap helpers for standalone scripts and app startup."""

# Import all model modules so SQLAlchemy registers string-based relationships.
from apps.auth import models as auth_models  # noqa: F401
from apps.organization import models as organization_models  # noqa: F401
from apps.employees import models as employee_models  # noqa: F401
from apps.requests import models as request_models  # noqa: F401
from apps.permissions import models as permission_models  # noqa: F401
