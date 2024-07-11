from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from farms.models import Farm


# Define user roles
USER_ROLES = (
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('User', 'User'),   
    )

class UserProfile(models.Model):
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    farms = models.ManyToManyField(Farm, blank=True, null=True)
    profile_img = models.CharField(max_length=255, blank=True, null=True)
    img_refference = models.CharField(max_length=255, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    token_created_at = models.DateTimeField(blank=True, null=True)
    role = models.CharField(max_length=255, choices=USER_ROLES, default="User")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email