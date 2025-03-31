from django.contrib import admin
from .models import Veterinarian, HealthCondition, VetService, HealthRecord, Treatment

@admin.register(Veterinarian)
class VeterinarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_number', 'specialization', 'farm')
    list_filter = ('farm', 'specialization')
    search_fields = ('name', 'contact_number', 'email')
    ordering = ('name',)

@admin.register(HealthCondition)
class HealthConditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'severity', 'is_contagious', 'farm')
    list_filter = ('severity', 'is_contagious', 'farm')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(VetService)
class VetServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_cost', 'farm')
    list_filter = ('farm',)
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('animal', 'condition', 'veterinarian', 'diagnosis_date', 'is_resolved')
    list_filter = ('is_resolved', 'condition', 'veterinarian', 'diagnosis_date')
    search_fields = ('animal__tag_number', 'animal__name', 'symptoms')
    ordering = ('-diagnosis_date',)
    readonly_fields = ('image_reference',)

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('health_record', 'service', 'treatment_date', 'quantity', 'total_cost')
    list_filter = ('service', 'treatment_date')
    search_fields = ('health_record__animal__tag_number', 'notes')
    ordering = ('-treatment_date',)
