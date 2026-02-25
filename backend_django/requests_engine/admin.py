from django.contrib import admin
from .models import RequestType, ApprovalWorkflow, ApprovalStep, Request, ApprovalHistory

# Register your models here.
admin.site.register(RequestType)
admin.site.register(ApprovalWorkflow)
admin.site.register(ApprovalStep)
admin.site.register(Request)
admin.site.register(ApprovalHistory)