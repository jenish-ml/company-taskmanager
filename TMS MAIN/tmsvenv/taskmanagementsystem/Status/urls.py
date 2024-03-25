from django.urls import path
from . import views

urlpatterns = [
    # path('add_status/<int:id>',views.statusadd),
    path('add_messages/<int:id>',views.statusadd),
    # path('add_status/<int:id>',views.statusesadd),
    # path('view_status',views.statusview),
    # path('view_status',views.statusesview),
    path('edit_status/<int:id>',views.statusedit),
    path('delete_status/<int:id>',views.statusdelete),
    path('view_task_statuses/<int:id>', views.taskstatusview, name='view_task_statuses'),
]