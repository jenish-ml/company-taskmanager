from django.db import models
from django.utils import timezone
from Authentication.models import Register 
from Team.models import *
from Files.models import UploadFile


class Projects(models.Model):
    title = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    current_date = models.DateField(default=timezone.now)
    created_by = models.ForeignKey(Register, on_delete=models.CASCADE, null=True)
    file = models.ManyToManyField(UploadFile, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    
    def __str__(self) -> str:
        return self.title
    