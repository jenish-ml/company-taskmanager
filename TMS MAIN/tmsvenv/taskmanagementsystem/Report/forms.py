from django import forms
from django.forms import ModelForm
from .models import *

class ReportForm(ModelForm):
    class Meta:
        model = Reports
        fields = ['start_date','end_date']
        widgets = {
            'start_date' : forms.TextInput(attrs={'class':'form-control2','type':'date'}),
            'end_date' : forms.TextInput(attrs={'class':'form-control2','type':'date'}),
        }
