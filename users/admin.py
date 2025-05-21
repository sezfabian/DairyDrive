from django.contrib import admin
from .models import UserProfile, SubscriptionPlan, UserSubscription, PaymentHistory
from import_export.admin import ImportExportModelAdmin


@admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'company', 'country', 'city', 'address', 'zip_code', 'currency', 'language', 'timezone', 'role', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    list_filter = ('company', 'role', 'created_at')
    filter_horizontal = ('farms',)
    ordering = ('-created_at',)

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    ordering = ('price',)

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'plan', 'start_date', 'end_date')
    search_fields = ('user__username', 'user__email', 'plan__name')
    ordering = ('-created_at',)

@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription', 'amount', 'status', 'payment_date')
    list_filter = ('status', 'payment_date')
    search_fields = ('user__username', 'user__email', 'stripe_payment_id')
    ordering = ('-payment_date',) 
