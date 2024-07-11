from .models import UserProfile
from farms.serializers import FarmSerializer
from django.contrib.auth.models import User
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer"""
    farms = FarmSerializer(many=True, read_only=True)  
    class Meta:
        model = UserProfile
        fields = ("email", "first_name", "last_name", "phone", "profile_img", "img_refference", "company", "farms", "user", "role")

class LoginSerializer(serializers.ModelSerializer):
    """Login serializer"""
    email_or_phone = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email_or_phone", "password")