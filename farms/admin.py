from django.contrib import admin
from .models import Farm
from import_export.admin import ImportExportModelAdmin


@admin.register(Farm)
class FarmAdmin(ImportExportModelAdmin):
    list_display = ('name', 'address', 'phone', 'coordinates', 'size', 'size_unit', 'description', 'code', 'created_by', 'created_at', 'updated_at')
    search_fields = ('name', 'phone')
