from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login", login, name="clientlogin"),
    path("signup", signup, name="user_register"),
    path("profile", get_profile, name="profile"),
]