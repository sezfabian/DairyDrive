from rest_framework import serializers
from .models import Product, ProductionRecord, Buyer, Sale
from animals.serializers import AnimalSerializer, AnimalTypeSerializer
from farms.serializers import FarmSerializer

class ProductSerializer(serializers.ModelSerializer):
    farm_details = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'unit', 'farm', 'farm_details', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_farm_details(self, obj):
        return FarmSerializer(obj.farm).data

class ProductionRecordSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()
    animal_details = serializers.SerializerMethodField()
    animal_type_details = serializers.SerializerMethodField()
    farm_details = serializers.SerializerMethodField()

    class Meta:
        model = ProductionRecord
        fields = [
            'id', 'product', 'product_details', 'farm', 'farm_details',
            'record_type', 'animal', 'animal_details', 'animal_type', 'animal_type_details',
            'quantity', 'date', 'time', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_product_details(self, obj):
        return ProductSerializer(obj.product).data

    def get_animal_details(self, obj):
        if obj.animal:
            return AnimalSerializer(obj.animal).data
        return None

    def get_animal_type_details(self, obj):
        if obj.animal_type:
            return AnimalTypeSerializer(obj.animal_type).data
        return None

    def get_farm_details(self, obj):
        return FarmSerializer(obj.farm).data

    def validate(self, data):
        if data['record_type'] == 'individual' and not data.get('animal'):
            raise serializers.ValidationError("Animal is required for individual records")
        if data['record_type'] == 'group' and not data.get('animal_type'):
            raise serializers.ValidationError("Animal type is required for group records")
        return data

class BuyerSerializer(serializers.ModelSerializer):
    farm_details = serializers.SerializerMethodField()

    class Meta:
        model = Buyer
        fields = [
            'id', 'name', 'contact_person', 'phone', 'email',
            'address', 'farm', 'farm_details', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_farm_details(self, obj):
        return FarmSerializer(obj.farm).data

class SaleSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()
    buyer_details = serializers.SerializerMethodField()
    farm_details = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = [
            'id', 'product', 'product_details', 'farm', 'farm_details',
            'buyer', 'buyer_details', 'quantity', 'unit_price', 'total_amount',
            'payment_method', 'payment_status', 'date', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['total_amount', 'created_at', 'updated_at']

    def get_product_details(self, obj):
        return ProductSerializer(obj.product).data

    def get_buyer_details(self, obj):
        return BuyerSerializer(obj.buyer).data

    def get_farm_details(self, obj):
        return FarmSerializer(obj.farm).data

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        if data['unit_price'] <= 0:
            raise serializers.ValidationError("Unit price must be greater than 0")
        return data 