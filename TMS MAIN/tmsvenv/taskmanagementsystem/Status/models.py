from django.db import models
from django.utils import timezone
from Project.models import *
from Tasks.models import *
from Files.models import *


class Status(models.Model):
    message = models.TextField(null=True)
    current_date = models.DateField(default=timezone.now)
    project = models.ForeignKey(Projects,on_delete=models.CASCADE,null=True)
    task = models.ForeignKey(Task,on_delete=models.CASCADE,null=True,related_name='+')
    file = models.ManyToManyField(UploadFile, blank=True)
    userid = models.ForeignKey(Register,on_delete=models.CASCADE,null=True,related_name="+")
    comments = models.TextField(null=True,blank=True)
    
    def __str__(self) -> str:
        return self.current_status
    
class Subtaskmessage(models.Model):
    message = models.TextField(null=True)
    current_date = models.DateField(default=timezone.now)
    project = models.ForeignKey(Projects,on_delete=models.CASCADE,null=True)
    task = models.ForeignKey(Task,on_delete=models.CASCADE,null=True,related_name='+')
    file = models.ManyToManyField(UploadFile, blank=True)
    userid = models.ForeignKey(Register,on_delete=models.CASCADE,null=True,related_name="+")
    
    def __str__(self) -> str:
        return self.current_status