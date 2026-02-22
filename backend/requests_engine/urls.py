from django.urls import path
from .api import (
    RequestTypeListCreateAPI,
    RequestTypeDetailAPI,
    ApprovalWorkflowListCreateAPI,
    ApprovalWorkflowDetailAPI,
    ApprovalStepListCreateAPI,
    ApprovalStepDetailAPI,
    RequestListCreateAPI,
    RequestDetailAPI,
    
)

urlpatterns = [
    # API endpoints for RequestType
    path('types/', RequestTypeListCreateAPI.as_view()),
    path('types/<int:pk>/', RequestTypeDetailAPI.as_view()),
    # API endpoints for ApprovalWorkflow
    path('workflows/', ApprovalWorkflowListCreateAPI.as_view()),
    path('workflows/<int:pk>/', ApprovalWorkflowDetailAPI.as_view()),
    # API endpoints for ApprovalStep
    path('steps/', ApprovalStepListCreateAPI.as_view()),
    path('steps/<int:pk>/', ApprovalStepDetailAPI.as_view()),
    # API endpoints for Request
    path('requests/', RequestListCreateAPI.as_view()),
    path('requests/<int:pk>/', RequestDetailAPI.as_view()),
]