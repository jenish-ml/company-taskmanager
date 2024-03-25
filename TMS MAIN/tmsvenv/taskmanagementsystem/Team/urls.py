from django.urls import path
from .import views

urlpatterns = [
    # path('add_team/',views.teamadd),
    # path('view_team',views.teamview),
    # path('edit_team/<int:id>',views.teamedit),
    # path('delete_team/<int:id>',views.teamdelete),
    # path('add_team_members/<int:id>',views.teammembersadd),
    # path('view_team_members',views.teammembersview),
    # path('edit_team_members/<int:id>',views.teammembersedit),
    # path('edit_project_team_members/<int:id>',views.teammembersprojectedit),
    # path('delete_team_members/<int:id>',views.teammembersdelete),
    # path('view_team_details/<int:id>',views.teammembersdetailsview),
    # path('view_team_members/<int:id>',views.teammemberview),
    path('project_teammembers_add',views.projectteammembersadd),
    path('project_teammembers_view',views.projectteammembersview),
    path('project_teammembers_edit/<int:id>',views.projectteammembersedit),
    path('project_teammembers_delete/<int:id>',views.projectteammembersdelete),
    path('project_team_edit/<int:id>',views.projectteamedit)
]