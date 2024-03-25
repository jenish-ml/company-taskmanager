from django import forms
from django.forms import ModelForm
from .models import *

ROLE_CHOICES =[
    ('','Select'),
    ('Manager','Manager'),
    ('Junior','Junior'),
    ('Senior','Senior'),
    ('Trainee','Trainee'),
]

class DesignationForm(ModelForm):
    class Meta:
        model = Role
        fields = ['role']
        widgets = {
            "role" : forms.TextInput(attrs={'class':'form-control2'})
        }
        
        