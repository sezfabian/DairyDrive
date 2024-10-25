from rest_framework import serializers
from django.db import transaction
from .models import AnimalFeedType, AnimalFeed, AnimalFeedEntry, AnimalFeedPurchase
from users.models import UserProfile

class AnimalFeedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalFeedType
        fields = ['id', 'name', 'farm']
        
class AnimalFeedSerializer(serializers.ModelSerializer):
    feed_type_name = serializers.SerializerMethodField()
    animal_types_names = serializers.SerializerMethodField()
    class Meta:
        model = AnimalFeed
        fields = ['id', 'name', 'description', 'animal_feed_type', 'feed_type_name', 'farm', 'unit', 'cost_per_unit', 'inventory', 'animal_types', 'animal_types_names']
    
    def get_feed_type_name(self, obj):
        return obj.animal_feed_type.name if obj.animal_feed_type else None
    
    def get_animal_types_names(self, obj):
        # Assuming animal_types is a related field with many-to-many relationship
        animal_types = obj.animal_types.all()  # Retrieve all related animal types
        animal_type_names = [animal_type.name for animal_type in animal_types]  # Get their names
        return 's, '.join(animal_type_names) + 's' # Join the names with commas
    
    def __str__(self):
        return self.name

class AnimalFeedEntrySerializer(serializers.ModelSerializer):
    animal_feed_name = serializers.SerializerMethodField()
    animal_type_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = AnimalFeedEntry
        fields = ['id', 'animal_feed', 'animal_feed_name', 'animal_type', 'animal_type_name', 'quantity', 'created_by','created_by_name', 'created_at', 'updated_at', 'is_deleted', 'deleted_by', 'deleted_at']
    
    def get_animal_feed_name(self, obj):
        return obj.animal_feed.name if obj.animal_feed else None
    
    def get_animal_type_name(self, obj):
        return obj.animal_type.name if obj.animal_type else None
    
    def get_created_by_name(self, obj):
        User = obj.created_by if obj.created_by else None
        name = UserProfile.objects.get(email=User.email).first_name
        return name
    

    def __str__(self):
        return f"{self.animal.name} - {self.animal_feed.name} - {self.quantity} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class AnimalFeedPurchaseSerializer(serializers.ModelSerializer):
    animal_feed_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = AnimalFeedPurchase
        fields = ['id', 'animal_feed', 'animal_feed_name', 'quantity', 'cost', 'created_by', 'created_by_name', 'created_at', 'updated_at', 'is_deleted', 'deleted_by', 'deleted_at']

    def get_animal_feed_name(self, obj):
        return obj.animal_feed.name if obj.animal_feed else None
    
    def get_created_by_name(self, obj):
        User = obj.created_by if obj.created_by else None
        name = UserProfile.objects.get(email=User.email).first_name
        return name

    def __str__(self):
        return f"{self.animal_feed.name} - {self.quantity} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"