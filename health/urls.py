from django.urls import path
from .views import *

urlpatterns = [
    # Veterinarians
    path("get_veterinarians/<int:farm_id>", get_veterinarians, name="get_veterinarians"),
    path("get_veterinarian/<int:farm_id>/<int:id>", get_veterinarian, name="get_veterinarian"),
    path("add_veterinarian/<int:farm_id>", add_veterinarian, name="add_veterinarian"),
    path("edit_veterinarian/<int:farm_id>/<int:id>", edit_veterinarian, name="edit_veterinarian"),
    path("delete_veterinarian/<int:farm_id>/<int:id>", delete_veterinarian, name="delete_veterinarian"),

    # Health Conditions
    path("get_health_conditions/<int:farm_id>", get_health_conditions, name="get_health_conditions"),
    path("get_health_condition/<int:farm_id>/<int:id>", get_health_condition, name="get_health_condition"),
    path("add_health_condition/<int:farm_id>", add_health_condition, name="add_health_condition"),
    path("edit_health_condition/<int:farm_id>/<int:id>", edit_health_condition, name="edit_health_condition"),
    path("delete_health_condition/<int:farm_id>/<int:id>", delete_health_condition, name="delete_health_condition"),

    # Vet Services
    path("get_vet_services/<int:farm_id>", get_vet_services, name="get_vet_services"),
    path("get_vet_service/<int:farm_id>/<int:id>", get_vet_service, name="get_vet_service"),
    path("add_vet_service/<int:farm_id>", add_vet_service, name="add_vet_service"),
    path("edit_vet_service/<int:farm_id>/<int:id>", edit_vet_service, name="edit_vet_service"),
    path("delete_vet_service/<int:farm_id>/<int:id>", delete_vet_service, name="delete_vet_service"),

    # Health Records
    path("get_health_records/<int:farm_id>", get_health_records, name="get_health_records"),
    path("get_health_record/<int:farm_id>/<int:id>", get_health_record, name="get_health_record"),
    path("add_health_record", add_health_record, name="add_health_record"),
    path("edit_health_record/<int:farm_id>/<int:id>", edit_health_record, name="edit_health_record"),
    path("delete_health_record/<int:farm_id>/<int:id>", delete_health_record, name="delete_health_record"),

    # Treatments
    path("get_treatments/<int:health_record_id>", get_treatments, name="get_treatments"),
    path("get_treatment/<int:farm_id>/<int:id>", get_treatment, name="get_treatment"),
    path("add_treatment", add_treatment, name="add_treatment"),
    path("edit_treatment/<int:farm_id>/<int:id>", edit_treatment, name="edit_treatment"),
    path("delete_treatment/<int:farm_id>/<int:id>", delete_treatment, name="delete_treatment"),
] 