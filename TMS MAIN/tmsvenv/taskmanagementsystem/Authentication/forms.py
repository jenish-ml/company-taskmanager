from django import forms
from django.forms import ModelForm
from .models import *
from Designation.models import Role



class LoginForm(ModelForm):
    class Meta:
        model=Register
        fields=['username','password']  
        help_texts = {
            'username' : None
        }
        
class StaffAddForm(ModelForm):
    
    designation = forms.ModelChoiceField(queryset=Role.objects.all())
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['designation'].widget.attrs['class'] = 'reg-form'
            
    class Meta:
        model = Register
        fields = ['name','email','contact','designation','password']
        widgets = {
            # "gender" : forms.Select(attrs={'class':'reg-form '},choices=GENDER_CHOICES),
            # "dob" : forms.DateInput(attrs={'class':'reg-form ','type':'date'}),
            "contact" : forms.TextInput(attrs={'class':'reg-form '}),
            "password" : forms.TextInput(attrs={'class':'reg-form ','type':'password'}),
        }    
        help_texts = {
            'username' : None
        }
        
        
class StaffEditForm(ModelForm):
    
    designation = forms.ModelChoiceField(queryset=Role.objects.all())
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['designation'].widget.attrs['class'] = 'reg-form'
            
    class Meta:
        model = Register
        fields = ['name','email','contact','designation']
        widgets = {
            # "gender" : forms.Select(attrs={'class':'reg-form '},choices=GENDER_CHOICES),
            # "dob" : forms.DateInput(attrs={'class':'reg-form ','type':'date'}),
            "contact" : forms.TextInput(attrs={'class':'reg-form '}),
        }    
        help_texts = {
            'username' : None
        }