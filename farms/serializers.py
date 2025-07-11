from .models import Farm, Transaction, Equipment, Expense, EquipmentPurchase
from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class FarmSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Farm
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('transaction_code', 'created_by', 'created_at', 'updated_at')

class EquipmentSerializer(serializers.ModelSerializer):
    farm_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = ['id', 'farm', 'farm_name', 'name', 'description', 'quantity', 'cost', 
                 'condition', 'purchase_date', 'last_maintenance_date', 'next_maintenance_date',
                 'created_by', 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ('created_by', 'created_at', 'updated_at')

    def get_farm_name(self, obj):
        return obj.farm.name if obj.farm else None

    def get_created_by_name(self, obj):
        if obj.created_by:
            profile = UserProfile.objects.get(email=obj.created_by.email)
            return f"{profile.first_name} {profile.last_name}"
        return None

class EquipmentPurchaseSerializer(serializers.ModelSerializer):
    farm_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    total_paid = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    pending_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = EquipmentPurchase
        fields = ['id', 'farm', 'farm_name', 'equipment_name', 'description', 'quantity', 
                 'unit_cost', 'total_cost', 'supplier', 'supplier_contact', 'purchase_date', 
                 'delivery_date', 'warranty_expiry', 'payment_method', 'payment_status', 
                 'due_date', 'payment_date', 'total_paid', 'pending_amount', 'transactions', 
                 'notes', 'created_by', 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ('payment_status', 'total_cost', 'created_by', 'created_at', 'updated_at')

    def get_farm_name(self, obj):
        return obj.farm.name if obj.farm else None

    def get_created_by_name(self, obj):
        if obj.created_by:
            profile = UserProfile.objects.get(email=obj.created_by.email)
            return f"{profile.first_name} {profile.last_name}"
        return None

    def validate(self, data):
        """Validate that total_cost is calculated correctly"""
        if 'unit_cost' in data and 'quantity' in data:
            calculated_total = data['unit_cost'] * data['quantity']
            if 'total_cost' in data and data['total_cost'] != calculated_total:
                raise serializers.ValidationError("Total cost must equal unit cost multiplied by quantity")
            data['total_cost'] = calculated_total
        return data

class ExpenseSerializer(serializers.ModelSerializer):
    farm_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    total_paid = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    pending_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'farm', 'farm_name', 'category', 'description', 'amount', 
                 'payment_status', 'due_date', 'payment_date', 'total_paid', 
                 'pending_amount', 'transactions', 'created_by', 'created_by_name', 
                 'created_at', 'updated_at']
        read_only_fields = ('payment_status', 'created_by', 'created_at', 'updated_at')

    def get_farm_name(self, obj):
        return obj.farm.name if obj.farm else None

    def get_created_by_name(self, obj):
        if obj.created_by:
            profile = UserProfile.objects.get(email=obj.created_by.email)
            return f"{profile.first_name} {profile.last_name}"
        return None