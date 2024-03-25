from django.db import models
from Designation.models import *
from django.contrib.auth.models import AbstractUser

class Register(AbstractUser):
    name = models.CharField(max_length=50,null=True)
    contact = models.IntegerField(null=True)
    usertype = models.IntegerField(null=True)
    status = models.IntegerField(default=0)
    designation = models.ForeignKey(Role,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.name
    