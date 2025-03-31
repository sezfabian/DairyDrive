from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup", signup, name="user_register"),
    path("login", login, name="clientlogin"),
    path("logout", logout, name="clientlogout"),
    path("profile", get_profile, name="profile"),
    path("edit_profile", edit_profile, name="edit_profile"),
    path("get_farm/<int:farm_id>", get_farm, name="get_farm"),
    path("get_subscription_plans", get_subscription_plans, name="get_subscription_plans"),
    path("create_subscription", create_subscription, name="create_subscription"),
    path("cancel_subscription", cancel_subscription, name="cancel_subscription"),
    path("get_subscription_status", get_subscription_status, name="get_subscription_status"),
    path("get_payment_history", get_payment_history, name="get_payment_history"),
]