from django.contrib import admin
# import all models
from .models import Departement, JobPosition, Team, UserProfile, LeaveAdjustment
# Register your models here.

# Register Departement model
admin.site.register(Departement)
# Register JobPosition model
admin.site.register(JobPosition)
# Register Team model
admin.site.register(Team)
# Register UserProfile model
admin.site.register(UserProfile)
# Register LeaveAdjustment model
admin.site.register(LeaveAdjustment)

