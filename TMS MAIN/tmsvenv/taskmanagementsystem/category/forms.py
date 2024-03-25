from django import forms
from django.forms import ModelForm
from .models import *

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['categories']
        widgets = {
            "categories" : forms.TextInput(attrs={'class':'form-control'})
        }