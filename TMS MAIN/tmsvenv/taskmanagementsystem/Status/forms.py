from django import forms
from django.forms import ModelForm
from .models import *


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
    
class StatusAddForm(ModelForm):
    file = MultipleFileField(required=False)
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control2', 'required': False}))
    class Meta:
        model = Status
        fields = ['message','file']
        
        
class StatusEditForm(ModelForm):
    file = MultipleFileField(required=False)
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control2', 'required': False}))
    class Meta:
        model = Status
        fields = ['message','file']
       
        
# class StatusesAddForm(ModelForm):
#     comments = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control2'}))
#     class Meta:
#         model = Task
#         fields = ['status','messages','comments']
#         widgets = {
#             'status' : forms.Select(choices=STATUS_CHOICES,attrs={'class':'form-control2'}),
#             'messages' : forms.Textarea(attrs={'class':'form-control2'})
#         }
        
# class StatusesEditForm(ModelForm):
#     comments = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control2'}))
#     class Meta:
#         model = Task
#         fields = ['status','messages','comments']
#         widgets = {
#             'status' : forms.Select(choices=STATUS_CHOICES,attrs={'class':'form-control2'}),
#             'messages' : forms.Textarea(attrs={'class':'form-control2'})
#         }