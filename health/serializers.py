from rest_framework import serializers
from .models import Veterinarian, HealthCondition, VetService, HealthRecord, Treatment
from animals.serializers import AnimalSerializer
from farms.serializers import FarmSerializer
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class VeterinarianSerializer(serializers.ModelSerializer):
    farm_name = serializers.SerializerMethodField()

    class Meta:
        model = Veterinarian
        fields = ['id', 'name', 'contact_number', 'email', 'address', 'specialization', 
                 'farm', 'farm_name', 'created_at', 'updated_at']

    def get_farm_name(self, obj):
        return obj.farm.name if obj.farm else None

class HealthConditionSerializer(serializers.ModelSerializer):
    farm_name = serializers.SerializerMethodField()

    class Meta:
        model = HealthCondition
        fields = ['id', 'name', 'description', 'severity', 'is_contagious', 
                 'farm', 'farm_name', 'created_at', 'updated_at']

    def get_farm_name(self, obj):
        return obj.farm.name if obj.farm else None

class VetServiceSerializer(serializers.ModelSerializer):
    farm_name = serializers.SerializerMethodField()

    class Meta:
        model = VetService
        fields = ['id', 'name', 'description', 'base_cost', 
                 'farm', 'farm_name', 'created_at', 'updated_at']

    def get_farm_name(self, obj):
        return obj.farm.name if obj.farm else None

class TreatmentSerializer(serializers.ModelSerializer):
    service_name = serializers.SerializerMethodField()
    animal_name = serializers.SerializerMethodField()
    health_record_condition = serializers.SerializerMethodField()

    class Meta:
        model = Treatment
        fields = ['id', 'health_record', 'service', 'service_name', 'health_record_condition',
                 'treatment_date', 'cost', 'notes', 'animal_name', 'created_at', 'updated_at']

    def get_service_name(self, obj):
        return obj.service.name if obj.service else None

    def get_animal_name(self, obj):
        return obj.health_record.animal.name if obj.health_record and obj.health_record.animal else None

    def get_health_record_condition(self, obj):
        return obj.health_record.condition.name if obj.health_record and obj.health_record.condition else None

class HealthRecordSerializer(serializers.ModelSerializer):
    animal_details = serializers.SerializerMethodField()
    condition_name = serializers.SerializerMethodField()
    veterinarian_name = serializers.SerializerMethodField()
    treatments = serializers.SerializerMethodField()

    class Meta:
        model = HealthRecord
        fields = ['id', 'animal', 'animal_details', 'condition', 'condition_name',
                 'veterinarian', 'veterinarian_name', 'diagnosis_date', 'symptoms',
                 'notes', 'is_resolved', 'resolution_date', 'treatments',
                 'image', 'image_reference', 'created_at', 'updated_at']

    def validate_image(self, value):
        if value:
            validator = URLValidator()
            try:
                validator(value)
            except ValidationError:
                raise serializers.ValidationError("Enter a valid URL for the image")
        return value

    def get_animal_details(self, obj):
        return AnimalSerializer(obj.animal).data if obj.animal else None

    def get_condition_name(self, obj):
        return obj.condition.name if obj.condition else None

    def get_veterinarian_name(self, obj):
        return obj.veterinarian.name if obj.veterinarian else None

    def get_treatments(self, obj):
        treatments = Treatment.objects.filter(health_record=obj)
        return TreatmentSerializer(treatments, many=True).data 