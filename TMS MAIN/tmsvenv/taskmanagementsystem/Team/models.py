from django.db import models
from Authentication.models import *
from Project.models import *

# Create your models here.
# class Teams(models.Model):
#     team_name = models.CharField(max_length=50)
    
    
# class Team_members(models.Model):
#     team_members = models.ManyToManyField(Register)
#     team = models.ForeignKey(Teams,on_delete=models.CASCADE,null=True)
#     def __str__(self) -> str:
#         return self.team.team_name

class Team(models.Model):
    team_name = models.CharField(max_length=50,null=True)
    team_members = models.ManyToManyField(Register)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.team_name
    