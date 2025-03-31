from rest_framework import serializers
from .models import Animal, AnimalImage, AnimalType, AnimalBreed, ArtificialInsemination

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

class AnimalSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    type_name = serializers.SerializerMethodField()
    breed_name = serializers.SerializerMethodField()
    ai_records = serializers.SerializerMethodField()
    ai_sire_details = serializers.SerializerMethodField()
    sire_type = serializers.SerializerMethodField()

    class Meta:
        model = Animal
        fields = [
            'id', 'name', 'type', 'type_name', 'breed', 'breed_name', 'gender', 'weight', 'description', 'age', 'date_of_birth', 'date_of_death',
            'dam', 'sire', 'ai_sire', 'ai_sire_details', 'sire_type', 'date_of_purchase', 'date_of_sale', 'is_on_sale', 'price',
            'purchase_price', 'farm', 'to_be_archived', 'created_by', 'created_at', 'updated_at',
            'images', 'ai_records'
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
