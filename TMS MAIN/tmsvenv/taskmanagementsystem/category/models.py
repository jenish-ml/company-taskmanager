from django.db import models

# Create your models here.
class Category(models.Model):
    categories = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.categories