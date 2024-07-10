from rest_framework import serializers
from .models import Animal, AnimalImage, AnimalType, AnimalBreed

class AnimalTypeSerializer(serializers.ModelSerializer):
    breeds = serializers.SerializerMethodField()
    class Meta:
        model = AnimalType
        fields = ['id', 'name', 'description', 'breeds']
    
    def get_breeds(self, obj):
        breeds = AnimalBreed.objects.filter(type=obj)
        return AnimalBreedSerializer(breeds, many=True).data

class AnimalBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalBreed
        fields = ['id', 'type', 'name', 'description']

class AnimalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalImage
        fields = ['id', 'image', 'uploaded_at']

class AnimalSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Animal
        fields = [
            'id', 'name', 'type', 'breed', 'description', 'age', 'date_of_birth', 'date_of_death',
            'dam', 'sire', 'date_of_purchase', 'date_of_sale', 'is_on_sale', 'price',
            'purchase_price', 'farm', 'to_be_archived', 'created_by', 'created_at', 'updated_at',
            'images'
        ]

    def get_images(self, obj):
        images = AnimalImage.objects.filter(animal=obj).order_by("id")[:10]
        return AnimalImageSerializer(images, many=True).data
