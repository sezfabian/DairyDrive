from django.contrib import admin
from .models import UserProfile
from import_export.admin import ImportExportModelAdmin


@admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'company', 'farms', 'role')
    search_fields = ('email', 'first_name', 'last_name', 'phone', 'company', 'farms', 'role')
    list_filter = ('email', 'first_name', 'last_name', 'phone', 'company', 'farms', 'role')
