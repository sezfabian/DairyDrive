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
    path("edit_farm/<int:id>", views.edit_farm, name="edit_farm"),
    path("delete_farm/<int:id>", views.delete_farm, name="delete_farm"),
    
    # Transaction URLs
    path("get_transactions", views.get_transactions, name="get_transactions"),
    path("create_transaction", views.create_transaction, name="create_transaction"),
    path("edit_transaction/<int:pk>", views.edit_transaction, name="edit_transaction"),
    path("delete_transaction/<int:pk>", views.delete_transaction, name="delete_transaction"),
    path("get_transaction/<int:pk>", views.get_transaction, name="get_transaction"),
    
    # Equipment URLs
    path("get_equipment", views.get_equipment, name="get_equipment"),
    path("create_equipment", views.create_equipment, name="create_equipment"),
    path("edit_equipment/<int:pk>", views.edit_equipment, name="edit_equipment"),
    path("delete_equipment/<int:pk>", views.delete_equipment, name="delete_equipment"),
    path("get_equipment/<int:pk>", views.get_equipment_detail, name="get_equipment_detail"),
    
    # Equipment Purchase URLs
    path("get_equipment_purchases", views.get_equipment_purchases, name="get_equipment_purchases"),
    path("create_equipment_purchase", views.create_equipment_purchase, name="create_equipment_purchase"),
    path("edit_equipment_purchase/<int:pk>", views.edit_equipment_purchase, name="edit_equipment_purchase"),
    path("delete_equipment_purchase/<int:pk>", views.delete_equipment_purchase, name="delete_equipment_purchase"),
    path("get_equipment_purchase/<int:pk>", views.get_equipment_purchase_detail, name="get_equipment_purchase_detail"),
    path("add_equipment_purchase_transaction/<int:pk>", views.add_equipment_purchase_transaction, name="add_equipment_purchase_transaction"),
    path("remove_equipment_purchase_transaction/<int:pk>", views.remove_equipment_purchase_transaction, name="remove_equipment_purchase_transaction"),
    
    # Expense URLs
    path("get_expenses", views.get_expenses, name="get_expenses"),
    path("create_expense", views.create_expense, name="create_expense"),
    path("edit_expense/<int:pk>", views.edit_expense, name="edit_expense"),
    path("delete_expense/<int:pk>", views.delete_expense, name="delete_expense"),
    path("get_expense/<int:pk>", views.get_expense_detail, name="get_expense_detail"),
    path("add_expense_transaction/<int:pk>", views.add_expense_transaction, name="add_expense_transaction"),
    path("remove_expense_transaction/<int:pk>", views.remove_expense_transaction, name="remove_expense_transaction"),
    
    # Include router URLs
    path('', include(router.urls)),
]