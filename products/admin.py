from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product, ProductionRecord, Buyer, Sale

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name', 'unit', 'farm', 'created_at')
    list_filter = ('farm', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

@admin.register(ProductionRecord)
class ProductionRecordAdmin(ImportExportModelAdmin):
    list_display = ('product', 'record_type', 'animal', 'animal_type', 'quantity', 'date', 'time')
    list_filter = ('farm', 'product', 'record_type', 'date')
    search_fields = ('product__name', 'animal__name', 'animal_type__name', 'notes')
    ordering = ('-date', '-time')

@admin.register(Buyer)
class BuyerAdmin(ImportExportModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'farm')
    list_filter = ('farm',)
    search_fields = ('name', 'contact_person', 'phone', 'email', 'address')
    ordering = ('name',)

@admin.register(Sale)
class SaleAdmin(ImportExportModelAdmin):
    list_display = ('product', 'buyer', 'quantity', 'unit_price', 'total_amount', 'payment_method', 'payment_status', 'date')
    list_filter = ('farm', 'product', 'buyer', 'payment_method', 'payment_status', 'date')
    search_fields = ('product__name', 'buyer__name', 'notes')
    ordering = ('-date',) 