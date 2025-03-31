from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

@admin.register(AnimalType)
class AnimalTypeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'description', 'created_by', 'created_at', 'updated_at')
    search_fields = ['name']

@admin.register(AnimalBreed)
class AnimalBreedAdmin(ImportExportModelAdmin):
    list_display = ('id', 'type', 'name', 'description', 'created_by', 'created_at', 'updated_at')
    search_fields = ['name']

@admin.register(Animal)
class AnimalAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'type', 'breed', 'gender', 'weight', 'description', 'farm', 'age', 'date_of_birth', 'date_of_death',
                    'dam', 'sire', 'date_of_purchase', 'date_of_sale', 'is_on_sale', 'price',
                    'purchase_price', 'to_be_archived', 'created_by', 'created_at', 'updated_at')
    search_fields = ['name']

@admin.register(AnimalImage)
class AnimalImageAdmin(ImportExportModelAdmin):
    list_display = ('id', 'animal', 'image_url', 'image_refference', 'created_at', 'updated_at')
    search_fields = ['animal__name']

@admin.register(ArtificialInsemination)
class ArtificialInseminationAdmin(ImportExportModelAdmin):
    list_display = ('animal', 'semen_code', 'breed', 'insemination_date', 'technician', 'status', 'cost')
    list_filter = ('status', 'breed', 'insemination_date', 'farm')
    search_fields = ('animal__name', 'semen_code', 'technician')
    ordering = ('-insemination_date',)