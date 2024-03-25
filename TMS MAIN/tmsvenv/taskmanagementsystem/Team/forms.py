from django import forms
from django.forms import ModelForm
from .models import *
from .models import *

# class TeamAddForm(ModelForm):
#     class Meta:
#         model = Teams
#         fields = ['team_name']

# class TeamMembersAddForm(ModelForm):
#     class Meta:
#         model = Team_members
#         fields = ['team_members']
#         widgets = {
#             'team_members': forms.CheckboxSelectMultiple()
#         }

#     def __init__(self, *args, **kwargs):
#         super(TeamMembersAddForm, self).__init__(*args, **kwargs)
#         self.fields['team_members'].queryset = Register.objects.exclude(usertype=1)
        
class ProjectTeamAddForm(ModelForm):
    class Meta:
        model = Team
        fields = ['team_name','team_members']
        widgets = {
            'team_members': forms.CheckboxSelectMultiple()
        }
    def __init__(self, *args, **kwargs):
        super(ProjectTeamAddForm, self).__init__(*args, **kwargs)
        self.fields['team_members'].queryset = Register.objects.exclude(usertype=1)