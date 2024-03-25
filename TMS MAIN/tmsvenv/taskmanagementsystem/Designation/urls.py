from django.urls import path
from .import views

urlpatterns = [
    path('role',views.designation),
    path('view_role',views.designation_view),
    path('edit_role/<int:id>',views.designation_edit),
    path('delete_role/<int:id>',views.designation_delete),
]