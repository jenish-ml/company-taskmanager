from django.urls import path
from .import views

urlpatterns = [
    path('add_category',views.add_category),
    path('view_category',views.view_category),
    path('edit_category/<int:id>',views.edit_category),
    path('delete_category/<int:id>',views.delete_category),
]