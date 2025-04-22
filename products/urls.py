from django.urls import path
from . import views

urlpatterns = [
    # Product URLs
    path('get_products/<int:farm_id>', views.get_products, name='get_products'),
    path('get_product/<int:farm_id>/<int:id>', views.get_product, name='get_product'),
    path('add_product/<int:farm_id>', views.add_product, name='add_product'),
    path('edit_product/<int:farm_id>/<int:id>', views.edit_product, name='edit_product'),
    path('delete_product/<int:farm_id>/<int:id>', views.delete_product, name='delete_product'),

    # Production Record URLs
    path('get_production_records/<int:farm_id>', views.get_production_records, name='get_production_records'),
    path('get_production_record/<int:farm_id>/<int:id>', views.get_production_record, name='get_production_record'),
    path('add_production_record/<int:farm_id>', views.add_production_record, name='add_production_record'),
    path('edit_production_record/<int:farm_id>/<int:id>', views.edit_production_record, name='edit_production_record'),
    path('delete_production_record/<int:farm_id>/<int:id>', views.delete_production_record, name='delete_production_record'),

    # Buyer URLs
    path('get_buyers/<int:farm_id>', views.get_buyers, name='get_buyers'),
    path('get_buyer/<int:farm_id>/<int:id>', views.get_buyer, name='get_buyer'),
    path('add_buyer/<int:farm_id>', views.add_buyer, name='add_buyer'),
    path('edit_buyer/<int:farm_id>/<int:id>', views.edit_buyer, name='edit_buyer'),
    path('delete_buyer/<int:farm_id>/<int:id>', views.delete_buyer, name='delete_buyer'),

    # Sale URLs
    path('get_sales/<int:farm_id>', views.get_sales, name='get_sales'),
    path('get_sale/<int:farm_id>/<int:id>', views.get_sale, name='get_sale'),
    path('add_sale/<int:farm_id>', views.add_sale, name='add_sale'),
    path('edit_sale/<int:farm_id>/<int:id>', views.edit_sale, name='edit_sale'),
    path('delete_sale/<int:farm_id>/<int:id>', views.delete_sale, name='delete_sale'),
    path('mark_sale_as_paid/<int:farm_id>/<int:id>', views.mark_sale_as_paid, name='mark_sale_as_paid'),
] 