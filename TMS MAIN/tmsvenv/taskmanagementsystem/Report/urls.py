from django.urls import path
from . import views

urlpatterns = [
    # path('task-report', views.task_report),
    # path('project-report', views.project_report),
    path('view_report/<int:id>', views.viewreport),
]