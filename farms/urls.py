from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Animal Type URLs
    path("get_farms", get_farms, name="get_farms"),
    path("create_farm", create_farm, name="create_farm"),
    path("edit_farm/<int:id>", edit_farm, name="edit_farm"),
    path("delete_farm/<int:id>", delete_farm, name="delete_farm"),
]