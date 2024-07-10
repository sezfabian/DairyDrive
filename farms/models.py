from django.db import models
from django.contrib.auth.models import User

class Farm(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    coordinates = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    size_unit = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name