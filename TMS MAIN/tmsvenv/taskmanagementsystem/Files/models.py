from django.db import models
from Authentication.models import Register 

class UploadFile(models.Model):
    file = models.FileField()
    def __str__(self) -> str:
        return self.file.name
