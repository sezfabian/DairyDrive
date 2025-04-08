from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Animal Types
    path("get_animal_types/<int:farm_id>", get_animal_types, name="get_animal_types"),
    path("add_animal_type/<int:farm_id>", add_animal_type, name="add_animal_type"),
    path("edit_animal_type/<int:farm_id>/<int:id>", edit_animal_type, name="edit_animal_type"),
    path("delete_animal_type/<int:farm_id>/<int:id>", delete_animal_type, name="delete_animal_type"),
    path("get_animal_breeds_by_type/<int:id>", get_animal_breeds_by_type, name="get_animal_breeds_by_type"),

    # Animal Breeds
    path("get_animal_breeds/<int:farm_id>", get_animal_breeds, name="get_animal_breeds"),
    path("add_animal_breed/<int:farm_id>", add_animal_breed, name="add_animal_breed"),
    path("edit_animal_breed/<int:farm_id>/<int:id>", edit_animal_breed, name="edit_animal_breed"),
    path("delete_animal_breed/<int:farm_id>/<int:id>", delete_animal_breed, name="delete_animal_breed"),

    # Animals
    path("get_animals/<int:farm_id>", get_animals, name="get_animals"),
    path("get_animal/<int:farm_id>/<int:id>", get_animal, name="get_animal"),
    path("create_animal/<int:farm_id>", add_animal, name="create_animal"),
    path("edit_animal/<int:farm_id>/<int:id>", edit_animal, name="edit_animal"),
    path("delete_animal/<int:farm_id>/<int:id>", delete_animal, name="delete_animal"),

    # Animal Images
    path("post_animal_image/<int:id>", post_animal_image, name="post_animal_image"),
    path("delete_animal_image/<int:farm_id>/<int:id>", delete_animal_image, name="delete_animal_image"),

    # Artificial Insemination
    path("get_ai_records/<int:farm_id>", get_ai_records, name="get_ai_records"),
    path("add_ai_record/<int:farm_id>", add_ai_record, name="add_ai_record"),
    path("edit_ai_record/<int:farm_id>/<int:id>", edit_ai_record, name="edit_ai_record"),
    path("delete_ai_record/<int:farm_id>/<int:id>", delete_ai_record, name="delete_ai_record"),
    path("set_ai_sire/<int:animal_id>", set_ai_sire, name="set_ai_sire"),
    path("clear_ai_sire/<int:animal_id>", clear_ai_sire, name="clear_ai_sire"),

    # Animal Health Records
    path("get_animal_health_records/<int:animal_id>", get_animal_health_records, name="get_animal_health_records"),
]