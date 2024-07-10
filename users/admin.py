from django.contrib import admin
from .models import UserProfile
from import_export.admin import ImportExportModelAdmin


@admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'company', 'role')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('company', 'role')
    filter_horizontal = ('farms',) 
