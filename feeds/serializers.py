from rest_framework import serializers
from django.db import transaction
from .models import AnimalFeedType, AnimalFeed, AnimalFeedEntry, AnimalFeedPurchase
from users.models import UserProfile
from django.db.models import Sum


class AnimalFeedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalFeedType
        fields = "__all__"
        
class AnimalFeedSerializer(serializers.ModelSerializer):
    feed_type_name = serializers.SerializerMethodField()
    animal_types_names = serializers.SerializerMethodField()
    
    # Use AnimalFeedTypeSerializer to serialize the related field
    animal_feed_type = serializers.PrimaryKeyRelatedField(queryset=AnimalFeedType.objects.all())

    class Meta:
        model = AnimalFeed
        fields = ['id', 'name', 'description', 'animal_feed_type', 'feed_type_name', 'farm', 'unit', 'cost_per_unit', 'inventory', 'animal_types', 'animal_types_names']
    
    def get_feed_type_name(self, obj):
        # Check if the object is a dict or a model instance
        if isinstance(obj, dict):
            # Retrieve the animal_feed_type from the dict (during input parsing)
            animal_feed_type_id = obj.get('animal_feed_type').id
            if animal_feed_type_id:
                try:
                    animal_feed_type = AnimalFeedType.objects.get(id=animal_feed_type_id)
                    return animal_feed_type.name  # Assuming `name` exists in AnimalFeedType
                except AnimalFeedType.DoesNotExist:
                    return None
            return None
        if obj.animal_feed_type:
            return obj.animal_feed_type.name  # Assuming the field `name` exists in AnimalFeedType
        return None
    
    def get_animal_types_names(self, obj):
        # Check whether the input is a dict (during input parsing) or a model instance
        if isinstance(obj, dict):
            animal_types = obj.get('animal_types')
        else:
            animal_types = obj.animal_types.all()  # Retrieve all related animal types

        # Extract the names from the animal types
        animal_type_names = [animal_type.name for animal_type in animal_types]  # Assuming `name` is a field in AnimalType
        return ', '.join(animal_type_names)  # Join the names with commas for display
    
    def __str__(self):
        return self.name

class AnimalFeedEntrySerializer(serializers.ModelSerializer):
    animal_feed_name = serializers.SerializerMethodField()
    inventory = serializers.SerializerMethodField()
    animal_type_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = AnimalFeedEntry
        fields = ['id', 'animal_feed', 'animal_feed_name', 'farm', 'inventory', 'cost_per_unit', 'total_cost', 'animal_type', 'animal_type_name', 'feed_date', 'feed_time', 'quantity', 'created_by','created_by_name', 'created_at', 'updated_at', 'is_deleted', 'deleted_by', 'deleted_at']
    
    def get_animal_feed_name(self, obj):
        return obj.animal_feed.name if obj.animal_feed else None
    
    def get_inventory(self, obj):
        return obj.animal_feed.inventory
    
    def get_animal_type_name(self, obj):
        return obj.animal_type.name if obj.animal_type else None
    
    def get_created_by_name(self, obj):
        User = obj.created_by if obj.created_by else None
        Profile = UserProfile.objects.get(email=User.email)
        name = Profile.first_name + " " + Profile.last_name
        return name
    

    def __str__(self):
        return f"{self.animal.name} - {self.animal_feed.name} - {self.quantity} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class AnimalFeedPurchaseSerializer(serializers.ModelSerializer):
    animal_feed_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    pending_payment = serializers.SerializerMethodField()
    is_paid = serializers.BooleanField(read_only=True)

    class Meta:
        model = AnimalFeedPurchase
        fields = ['id', 'animal_feed', 'animal_feed_name', 'farm', 'quantity', 'cost', 'pending_payment', 'is_paid', 'created_by', 'created_by_name', 'created_at', 'updated_at', 'is_deleted', 'deleted_by', 'deleted_at']

    def get_animal_feed_name(self, obj):
        return obj.animal_feed.name if obj.animal_feed else None
    
    def get_created_by_name(self, obj):
        User = obj.created_by if obj.created_by else None
        name = UserProfile.objects.get(email=User.email).first_name
        return name

    def get_pending_payment(self, obj):
        total_paid = obj.transactions.filter(transaction_type='incoming').aggregate(total=Sum('amount'))['total'] or 0
        pending = obj.cost - total_paid
        return max(0, pending)  # Return 0 if pending is negative

    def __str__(self):
        return f"{self.animal_feed.name} - {self.quantity} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"