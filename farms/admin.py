from django.contrib import admin
from .models import Farm, Transaction, Equipment, Expense
from import_export.admin import ImportExportModelAdmin


@admin.register(Farm)
class FarmAdmin(ImportExportModelAdmin):
    list_display = ('name', 'address', 'phone', 'coordinates', 'size', 'size_unit', 'description', 'code', 'created_by', 'created_at', 'updated_at')
    search_fields = ('name', 'phone')

@admin.register(Equipment)
class EquipmentAdmin(ImportExportModelAdmin):
    list_display = ('name', 'farm', 'quantity', 'cost', 'condition', 'purchase_date', 'last_maintenance_date', 'next_maintenance_date', 'created_by', 'created_at')
    list_filter = ('condition', 'farm', 'created_at')
    search_fields = ('name', 'description', 'farm__name')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Expense)
class ExpenseAdmin(ImportExportModelAdmin):
    list_display = ('category', 'farm', 'amount', 'payment_status', 'due_date', 'payment_date', 'created_by', 'created_at')
    list_filter = ('category', 'payment_status', 'farm', 'created_at')
    search_fields = ('description', 'farm__name', 'category')
    date_hierarchy = 'created_at'
    readonly_fields = ('payment_status', 'created_at', 'updated_at')

@admin.register(Transaction)
class TransactionAdmin(ImportExportModelAdmin):
    list_display = ('transaction_type', 'farm', 'amount', 'payment_method', 'transaction_date', 'created_by', 'created_at')
    list_filter = ('transaction_type', 'payment_method', 'farm', 'created_at')
    search_fields = ('description', 'farm__name', 'transaction_code')
    date_hierarchy = 'created_at'
    readonly_fields = ('transaction_code', 'created_at', 'updated_at')
