from rest_framework import serializers
from .models import Animal, AnimalImage, AnimalType, AnimalBreed, ArtificialInsemination
from health.models import HealthRecord, Treatment, VetService

class AnimalTypeSerializer(serializers.ModelSerializer):
    breeds = serializers.SerializerMethodField()
    class Meta:
        model = AnimalType
        fields = ['id', 'name', 'farm', 'description', 'breeds']
    
    def get_breeds(self, obj):
        breeds = AnimalBreed.objects.filter(type=obj)
        return AnimalBreedSerializer(breeds, many=True).data

class AnimalBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalBreed
        fields = ['id', 'type', 'name', 'farm', 'description']

class AnimalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalImage
        fields = ['id', 'image_url', 'image_refference', 'animal', 'created_at', 'updated_at']

class ArtificialInseminationSerializer(serializers.ModelSerializer):
    animal_name = serializers.SerializerMethodField()
    breed_name = serializers.SerializerMethodField()

    class Meta:
        model = ArtificialInsemination
        fields = [
            'id', 'animal', 'animal_name', 'semen_code', 'breed', 'breed_name',
            'insemination_date', 'technician', 'status', 'cost', 'notes',
            'farm', 'created_by', 'created_at', 'updated_at'
        ]

    def get_animal_name(self, obj):
        return obj.animal.name if obj.animal else None

    def get_breed_name(self, obj):
        return obj.breed.name if obj.breed else None

class TreatmentSerializer(serializers.ModelSerializer):
    service_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Treatment
        fields = [
            'id', 'service', 'service_name', 'treatment_date', 'quantity',
            'unit_cost', 'total_cost', 'notes', 'created_at', 'updated_at'
        ]
    
    def get_service_name(self, obj):
        return obj.service.name if obj.service else None

class HealthRecordSerializer(serializers.ModelSerializer):
    condition_name = serializers.SerializerMethodField()
    veterinarian_name = serializers.SerializerMethodField()
    treatments = TreatmentSerializer(many=True, read_only=True)

    class Meta:
        model = HealthRecord
        fields = [
            'id', 'animal', 'condition', 'condition_name', 'veterinarian', 'veterinarian_name',
            'diagnosis_date', 'symptoms', 'notes', 'is_resolved', 'resolution_date',
            'image', 'image_reference', 'treatments', 'created_at', 'updated_at'
        ]

    def get_condition_name(self, obj):
        return obj.condition.name if obj.condition else None

    def get_veterinarian_name(self, obj):
        return obj.veterinarian.name if obj.veterinarian else None

class AnimalSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    type_name = serializers.SerializerMethodField()
    breed_name = serializers.SerializerMethodField()
    ai_records = serializers.SerializerMethodField()
    ai_sire_details = serializers.SerializerMethodField()
    sire_type = serializers.SerializerMethodField()
    health_records = serializers.SerializerMethodField()

    class Meta:
        model = Animal
        fields = [
            'id', 'name', 'type', 'type_name', 'breed', 'breed_name', 'gender', 'weight', 'description', 'age', 'date_of_birth', 'date_of_death',
            'dam', 'sire', 'ai_sire', 'ai_sire_details', 'sire_type', 'date_of_purchase', 'date_of_sale', 'is_on_sale', 'price',
            'purchase_price', 'farm', 'to_be_archived', 'created_by', 'created_at', 'updated_at',
            'images', 'ai_records', 'health_records'
        ]

    def get_images(self, obj):
        images = AnimalImage.objects.filter(animal=obj).order_by("-id")[:10]
        return AnimalImageSerializer(images, many=True).data
    
    def get_type_name(self, obj):
        return obj.type.name if obj.type else None
    
    def get_breed_name(self, obj):
        return obj.breed.name if obj.breed else None

    def get_ai_records(self, obj):
        ai_records = ArtificialInsemination.objects.filter(animal=obj).order_by('-insemination_date')
        return ArtificialInseminationSerializer(ai_records, many=True).data

    def get_ai_sire_details(self, obj):
        if obj.ai_sire:
            return ArtificialInseminationSerializer(obj.ai_sire).data
        return None

    def get_sire_type(self, obj):
        if obj.ai_sire:
            return 'AI'
        elif obj.sire:
            return 'Natural'
        return None

    def get_health_records(self, obj):
        health_records = HealthRecord.objects.filter(animal=obj).order_by('-diagnosis_date')
        return HealthRecordSerializer(health_records, many=True).data
