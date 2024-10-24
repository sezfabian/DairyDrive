from rest_framework import serializers
from django.db import transaction
from .models import AnimalFeedType, AnimalFeed, AnimalFeedEntry, AnimalFeedPurchase

class AnimalFeedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalFeedType
        fields = ['id', 'name', 'farm']
        
class AnimalFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalFeed
        fields = ['id', 'name', 'description', 'animal_feed_type', 'farm', 'unit', 'cost_per_unit', 'inventory', 'animal_types']

    def __str__(self):
        return self.name

class AnimalFeedEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalFeedEntry
        fields = ['id', 'animal_feed', 'animal_type', 'quantity', 'created_by', 'created_at', 'updated_at', 'is_deleted', 'deleted_by', 'deleted_at']
    
    # On save decrease animal feed inventory 

    def __str__(self):
        return f"{self.animal.name} - {self.animal_feed.name} - {self.quantity} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class AnimalFeedPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalFeedPurchase
        fields = ['id', 'animal_feed', 'quantity', 'cost', 'created_by', 'created_at', 'updated_at', 'is_deleted', 'deleted_by', 'deleted_at']

    def __str__(self):
        return f"{self.animal_feed.name} - {self.quantity} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"