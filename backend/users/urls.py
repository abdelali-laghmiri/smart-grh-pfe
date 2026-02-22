from django.urls import path
from .api import DepartmentListCreateAPI, DepartmentDetailAPI, JobPositionListCreateAPI, JobPositionDetailAPI

urlpatterns = [
    path('departments/', DepartmentListCreateAPI.as_view()),
    path('departments/<int:pk>/', DepartmentDetailAPI.as_view()),
    path('positions/', JobPositionListCreateAPI.as_view()),
    path('positions/<int:pk>/', JobPositionDetailAPI.as_view()),
]