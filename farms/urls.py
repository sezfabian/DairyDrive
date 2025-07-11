from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'farms', views.FarmViewSet)
router.register(r'transactions', views.TransactionViewSet, basename='transaction')

urlpatterns = [
    # Farm URLs
    path("get_farms", views.get_farms, name="get_farms"),
    path("create_farm", views.create_farm, name="create_farm"),
    path("get_farm/<int:farm_id>", views.get_farm, name="get_farm"),
    path("edit_farm/<int:farm_id>", views.edit_farm, name="edit_farm"),
    path("delete_farm/<int:farm_id>", views.delete_farm, name="delete_farm"),
    
    # Transaction URLs
    path("get_transactions/<int:farm_id>", views.get_transactions, name="get_transactions"),
    path("add_transaction/<int:farm_id>", views.create_transaction, name="create_transaction"),
    path("edit_transaction/<int:farm_id>/<int:pk>", views.edit_transaction, name="edit_transaction"),
    path("delete_transaction/<int:farm_id>/<int:pk>", views.delete_transaction, name="delete_transaction"),
    path("get_transaction/<int:farm_id>/<int:pk>", views.get_transaction, name="get_transaction"),
    
    # Equipment URLs
    path("get_equipment/<int:farm_id>", views.get_equipment, name="get_equipment"),
    path("add_equipment/<int:farm_id>", views.create_equipment, name="create_equipment"),
    path("edit_equipment/<int:farm_id>/<int:pk>", views.edit_equipment, name="edit_equipment"),
    path("delete_equipment/<int:farm_id>/<int:pk>", views.delete_equipment, name="delete_equipment"),
    path("get_equipment_item/<int:farm_id>/<int:pk>", views.get_equipment_detail, name="get_equipment_detail"),
    
    # Equipment Purchase URLs
    path("get_equipment_purchases/<int:farm_id>", views.get_equipment_purchases, name="get_equipment_purchases"),
    path("add_equipment_purchase/<int:farm_id>", views.create_equipment_purchase, name="create_equipment_purchase"),
    path("edit_equipment_purchase/<int:farm_id>/<int:pk>", views.edit_equipment_purchase, name="edit_equipment_purchase"),
    path("delete_equipment_purchase/<int:farm_id>/<int:pk>", views.delete_equipment_purchase, name="delete_equipment_purchase"),
    path("get_equipment_purchase/<int:farm_id>/<int:pk>", views.get_equipment_purchase_detail, name="get_equipment_purchase_detail"),
    path("add_equipment_purchase_transaction/<int:farm_id>/<int:pk>", views.add_equipment_purchase_transaction, name="add_equipment_purchase_transaction"),
    path("remove_equipment_purchase_transaction/<int:farm_id>/<int:pk>", views.remove_equipment_purchase_transaction, name="remove_equipment_purchase_transaction"),
    
    # Expense URLs
    path("get_expenses/<int:farm_id>", views.get_expenses, name="get_expenses"),
    path("add_expense/<int:farm_id>", views.create_expense, name="create_expense"),
    path("edit_expense/<int:farm_id>/<int:pk>", views.edit_expense, name="edit_expense"),
    path("delete_expense/<int:farm_id>/<int:pk>", views.delete_expense, name="delete_expense"),
    path("get_expense/<int:farm_id>/<int:pk>", views.get_expense_detail, name="get_expense_detail"),
    path("add_expense_transaction/<int:farm_id>/<int:pk>", views.add_expense_transaction, name="add_expense_transaction"),
    path("remove_expense_transaction/<int:farm_id>/<int:pk>", views.remove_expense_transaction, name="remove_expense_transaction"),
    
    # Expense Categories URLs
    path("get_expense_categories/<int:farm_id>", views.get_expense_categories, name="get_expense_categories"),
    path("add_expense_category/<int:farm_id>", views.create_expense_category, name="create_expense_category"),
    path("edit_expense_category/<int:farm_id>/<int:pk>", views.edit_expense_category, name="edit_expense_category"),
    path("delete_expense_category/<int:farm_id>/<int:pk>", views.delete_expense_category, name="delete_expense_category"),
    
    # Farm Statistics URLs
    path("get_farm_statistics/<int:farm_id>", views.get_farm_statistics, name="get_farm_statistics"),
    path("get_farm_income/<int:farm_id>", views.get_farm_income, name="get_farm_income"),
    path("get_farm_expenses/<int:farm_id>", views.get_farm_expenses, name="get_farm_expenses"),
    
    # Farm Users URLs
    path("get_farm_users/<int:farm_id>", views.get_farm_users, name="get_farm_users"),
    path("add_farm_user/<int:farm_id>", views.add_farm_user, name="add_farm_user"),
    path("remove_farm_user/<int:farm_id>/<int:user_id>", views.remove_farm_user, name="remove_farm_user"),
    
    # Farm Settings URLs
    path("get_farm_settings/<int:farm_id>", views.get_farm_settings, name="get_farm_settings"),
    path("update_farm_settings/<int:farm_id>", views.update_farm_settings, name="update_farm_settings"),
    
    # Include router URLs
    path('', include(router.urls)),
]