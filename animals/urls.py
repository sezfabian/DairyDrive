from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Animal types
    path("get_animal_types", get_animal_types, name="get_animal_types"),
    path("add_animal_type", add_animal_type, name="create_animal_type"),
    path("edit_animal_type/<int:id>", edit_animal_type, name="edit_animal_type"),
    path("delete_animal_type/<int:id>", delete_animal_type, name="delete_animal_type"),
    path("get_animal_breeds_by_type/<int:id>", get_animal_breeds_by_type, name="get_animal_breeds_by_type"),

    # Animal breeds
    path("get_animal_breeds", get_animal_breeds, name="get_animal_breeds"),
    path("add_animal_breed", add_animal_breed, name="create_animal_breed"),
    path("edit_animal_breed", edit_animal_breed, name="edit_animal_breed"),
    path("delete_animal_breed", delete_animal_breed, name="delete_animal_breed"),

    # Animals
    path("get_animals", get_animals, name="get_animals"),
    path("get_animal/<int:id>", get_animal, name="get_animal"),
    path("create_animal", create_animal, name="create_animal"),
    path("edit_animal", edit_animal, name="edit_animal"),
    path("delete_animal", delete_animal, name="delete_animal"),
]