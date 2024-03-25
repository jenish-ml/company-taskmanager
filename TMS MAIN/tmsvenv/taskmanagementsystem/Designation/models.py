from django.db import models

# Create your models here.
class Role(models.Model):
    role = models.CharField(null=True,max_length=100)
    def __str__(self) -> str:
        return self.role