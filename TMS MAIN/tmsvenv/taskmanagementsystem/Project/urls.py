from django.urls import path
from .import views

urlpatterns = [
    path('add_project',views.projectadd),
    path('view_project',views.projectview ),
    path('view_staff_project_index',views.view_staff_project_index, name='view_staff_project_index' ),
    path('edit_project/<int:id>',views.projectedit),
    path('delete_project/<int:id>',views.projectdelete),
    path('view_project_index/<int:id>/',views.projectviewindex ,name='view_project_index'),
    # path('view_project_changes', views.view_project_changes, name='view_project_changes'),
]