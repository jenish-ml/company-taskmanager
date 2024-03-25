from django.urls import path
from . import views

urlpatterns = [
    path('add_task/<int:id>/',views.taskadd),
    path('apply_status/<int:id>/',views.statusupdate),
    path('add_subtask/<int:id>/',views.subtaskadd),
    path('add_subtask_message/<int:id>/',views.subtaskmessage),
    path('view_task/<int:id>',views.view_main_task ,name='view_task'),
    path('view_subtasks/<int:id>',views.subtaskview ,name='view_subtask'),
    path('delete_task/<int:id>',views.taskdelete),
    path('delete_subtask/<int:id>',views.subtaskdelete),
    path('edit_task/<int:id>',views.taskedit),
    path('edit_subtask/<int:id>',views.subtaskedit),
    path('view_project_details/<int:id>',views.view_project_details),
    path('view_project_task/<int:id>', views.taskprojectview, name='view_project_task'),
    # path('view_tasks',views.task_performance_analysises),
    # path('view_project_task_performance/<int:project_id>/', views.task_performance_analysis, name='view_project_task_performance'),
]