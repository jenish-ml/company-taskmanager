from django import forms
from django.forms import ModelForm
from .models import *
from Status.models import *

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]

CATEGORY_CHOICES = [
    ('task', 'Task'),
    ('bug', 'Bug'),
    ('defect', 'Defect'),
]
        
STATUS_CHOICES = [
    ('', 'Select'),
    ('New', 'New'),
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
    ('Resolved', 'Resolved'),
    ('Reopen', 'Reopen'),
]

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

class TaskEditForm(forms.ModelForm):
    file = MultipleFileField()
    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date', 'due_date', 'priority', 'category','file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control2'}),
            'description': forms.Textarea(attrs={'class': 'form-control2'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control2', 'type': 'date'}),
            'due_date': forms.TextInput(attrs={'class': 'form-control2', 'type': 'date'}),
            'priority': forms.Select(choices=PRIORITY_CHOICES, attrs={'class': 'form-control2'}),
            'category': forms.Select(choices=CATEGORY_CHOICES,attrs={'class': 'form-control2'}),
            # 'status': forms.Select(choices=STATUS_CHOICES,attrs={'class': 'form-control2'}),
        }
        
class SubTaskEditForm(forms.ModelForm):
    file = MultipleFileField()   
    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date', 'due_date', 'priority', 'category','file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control2'}),
            'description': forms.Textarea(attrs={'class': 'form-control2'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control2', 'type': 'date'}),
            'due_date': forms.TextInput(attrs={'class': 'form-control2', 'type': 'date'}),
            'priority': forms.Select(choices=PRIORITY_CHOICES, attrs={'class': 'form-control2'}),
            'category': forms.Select(choices=CATEGORY_CHOICES,attrs={'class': 'form-control2'}),
        }

class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=STATUS_CHOICES,attrs={'class': 'form-control2'})
        }
        
class MessageAddForm(ModelForm):
    file = MultipleFileField()
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control2', 'required': False}))
    class Meta:
        model = Subtaskmessage
        fields = ['message','file']