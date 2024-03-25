from django.urls import path
from .import views

urlpatterns = [
    path('',views.index),
    path('login',views.dologin),
    path('logout',views.dologout),
    path('add_staff',views.staffadd),
    path('view_staff',views.staffview),
    path('edit_staff/<int:id>',views.staffedit),
    path('delete_staff/<int:id>',views.staffdelete),
]