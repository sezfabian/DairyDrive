from django.contrib.auth.models import User
from users.functions import fix_phone_number
from .serializers import *
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
import random
from rest_framework import viewsets, permissions
from .models import Farm, Transaction, Equipment, Expense, EquipmentPurchase
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta


@api_view(['GET'])
def get_farms(request):
    """Get farms"""
    farms = Farm.objects.all()
    serializer = FarmSerializer(farms, many=True)
    return Response(serializer.data, status=200)


@api_view(['POST'])
def create_farm(request):
    """Create farm"""
    generated_code = random.randint(1000, 9999)
    request.data["created_by"] = request.user.id
    request.data["code"] = request.data["name"].upper()[0] + "F" + str(generated_code)
    request.data["phone"] = fix_phone_number(request.data["phone"])
    serializer = FarmSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_farm(request, farm_id):
    """Get specific farm"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        serializer = FarmSerializer(farm)
        return Response(serializer.data, status=200)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)

@api_view(['POST'])
def edit_farm(request, farm_id):
    """Edit farm"""
    request.data["phone"] = fix_phone_number(request.data["phone"])
    request.data["created_by"] = request.user.id

    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)
    
    # Ensure we're not creating a new farm with the same name
    if farm.name == request.data.get("name"):
        request.data.pop("name", None)

    serializer = FarmSerializer(farm, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def delete_farm(request, farm_id):
    """Delete farm"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        farm.delete()
        return Response({"message": f"Farm id:{farm_id} deleted successfully"}, status=200)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)

# Transaction specific views
@api_view(['GET'])
def get_transactions(request, farm_id):
    """Get all transactions for specific farm"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        transactions = Transaction.objects.filter(farm=farm)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=200)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)

@api_view(['POST'])
def create_transaction(request, farm_id):
    """Create a new transaction"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        request.data["farm"] = farm_id
        request.data["created_by"] = request.user.id
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)

@api_view(['POST'])
def edit_transaction(request, farm_id, pk):
    """Edit an existing transaction"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        transaction = Transaction.objects.get(pk=pk, farm=farm)
    except (Farm.DoesNotExist, Transaction.DoesNotExist):
        return Response({"message": f"Transaction id:{pk} not found"}, status=404)

    serializer = TransactionSerializer(transaction, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def delete_transaction(request, farm_id, pk):
    """Delete a transaction"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        transaction = Transaction.objects.get(pk=pk, farm=farm)
        transaction.delete()
        return Response({"message": f"Transaction id:{pk} deleted successfully"}, status=200)
    except (Farm.DoesNotExist, Transaction.DoesNotExist):
        return Response({"message": f"Transaction id:{pk} not found"}, status=404)

@api_view(['GET'])
def get_transaction(request, farm_id, pk):
    """Get a specific transaction"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        transaction = Transaction.objects.get(pk=pk, farm=farm)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=200)
    except (Farm.DoesNotExist, Transaction.DoesNotExist):
        return Response({"message": f"Transaction id:{pk} not found"}, status=404)

# ViewSets
class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(farm__created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# Equipment Views
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_equipment(request, farm_id):
    """Get all equipment for specific farm"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        equipment = Equipment.objects.filter(farm=farm)
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_equipment(request, farm_id):
    """Create new equipment"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        request.data['farm'] = farm_id
        request.data['created_by'] = request.user.id
        serializer = EquipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def edit_equipment(request, farm_id, pk):
    """Edit existing equipment"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        equipment = Equipment.objects.get(pk=pk, farm=farm)
        serializer = EquipmentSerializer(equipment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except (Farm.DoesNotExist, Equipment.DoesNotExist):
        return Response({"message": f"Equipment id:{pk} not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def delete_equipment(request, farm_id, pk):
    """Delete equipment"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        equipment = Equipment.objects.get(pk=pk, farm=farm)
        equipment.delete()
        return Response(status=204)
    except (Farm.DoesNotExist, Equipment.DoesNotExist):
        return Response({"message": f"Equipment id:{pk} not found"}, status=404)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_equipment_detail(request, farm_id, pk):
    """Get specific equipment details"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        equipment = Equipment.objects.get(pk=pk, farm=farm)
        serializer = EquipmentSerializer(equipment)
        return Response(serializer.data)
    except (Farm.DoesNotExist, Equipment.DoesNotExist):
        return Response({"message": f"Equipment id:{pk} not found"}, status=404)

# Expense Views
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_expenses(request, farm_id):
    """Get all expenses for specific farm"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        expenses = Expense.objects.filter(farm=farm)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_expense(request, farm_id):
    """Create new expense"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        request.data['farm'] = farm_id
        request.data['created_by'] = request.user.id
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def edit_expense(request, farm_id, pk):
    """Edit existing expense"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        expense = Expense.objects.get(pk=pk, farm=farm)
        serializer = ExpenseSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except (Farm.DoesNotExist, Expense.DoesNotExist):
        return Response({"message": f"Expense id:{pk} not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def delete_expense(request, farm_id, pk):
    """Delete expense"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        expense = Expense.objects.get(pk=pk, farm=farm)
        expense.delete()
        return Response(status=204)
    except (Farm.DoesNotExist, Expense.DoesNotExist):
        return Response({"message": f"Expense id:{pk} not found"}, status=404)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_expense_detail(request, farm_id, pk):
    """Get specific expense details"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        expense = Expense.objects.get(pk=pk, farm=farm)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)
    except (Farm.DoesNotExist, Expense.DoesNotExist):
        return Response({"message": f"Expense id:{pk} not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_expense_transaction(request, farm_id, pk):
    """Add a transaction to an expense"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        expense = Expense.objects.get(pk=pk, farm=farm)
        transaction = Transaction.objects.get(pk=request.data.get('transaction_id'))
        
        if transaction.farm != expense.farm:
            return Response({"error": "Transaction must be from the same farm"}, status=400)
        
        expense.add_transaction(transaction)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)
    except (Farm.DoesNotExist, Expense.DoesNotExist, Transaction.DoesNotExist):
        return Response({"message": "Resource not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def remove_expense_transaction(request, farm_id, pk):
    """Remove a transaction from an expense"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        expense = Expense.objects.get(pk=pk, farm=farm)
        transaction = Transaction.objects.get(pk=request.data.get('transaction_id'))
        
        expense.remove_transaction(transaction)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)
    except (Farm.DoesNotExist, Expense.DoesNotExist, Transaction.DoesNotExist):
        return Response({"message": "Resource not found"}, status=404)

# Equipment Purchase Views
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_equipment_purchases(request, farm_id):
    """Get all equipment purchases for specific farm"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        purchases = EquipmentPurchase.objects.filter(farm=farm)
        serializer = EquipmentPurchaseSerializer(purchases, many=True)
        return Response(serializer.data)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_equipment_purchase(request, farm_id):
    """Create new equipment purchase"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        request.data['farm'] = farm_id
        request.data['created_by'] = request.user.id
        serializer = EquipmentPurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def edit_equipment_purchase(request, farm_id, pk):
    """Edit existing equipment purchase"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        purchase = EquipmentPurchase.objects.get(pk=pk, farm=farm)
        serializer = EquipmentPurchaseSerializer(purchase, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except (Farm.DoesNotExist, EquipmentPurchase.DoesNotExist):
        return Response({"message": f"Equipment purchase id:{pk} not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def delete_equipment_purchase(request, farm_id, pk):
    """Delete equipment purchase"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        purchase = EquipmentPurchase.objects.get(pk=pk, farm=farm)
        purchase.delete()
        return Response(status=204)
    except (Farm.DoesNotExist, EquipmentPurchase.DoesNotExist):
        return Response({"message": f"Equipment purchase id:{pk} not found"}, status=404)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_equipment_purchase_detail(request, farm_id, pk):
    """Get specific equipment purchase details"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        purchase = EquipmentPurchase.objects.get(pk=pk, farm=farm)
        serializer = EquipmentPurchaseSerializer(purchase)
        return Response(serializer.data)
    except (Farm.DoesNotExist, EquipmentPurchase.DoesNotExist):
        return Response({"message": f"Equipment purchase id:{pk} not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_equipment_purchase_transaction(request, farm_id, pk):
    """Add a transaction to an equipment purchase"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        purchase = EquipmentPurchase.objects.get(pk=pk, farm=farm)
        transaction = Transaction.objects.get(pk=request.data.get('transaction_id'))
        
        if transaction.farm != purchase.farm:
            return Response({"error": "Transaction must be from the same farm"}, status=400)
        
        purchase.add_transaction(transaction)
        serializer = EquipmentPurchaseSerializer(purchase)
        return Response(serializer.data)
    except (Farm.DoesNotExist, EquipmentPurchase.DoesNotExist, Transaction.DoesNotExist):
        return Response({"message": "Resource not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def remove_equipment_purchase_transaction(request, farm_id, pk):
    """Remove a transaction from an equipment purchase"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        purchase = EquipmentPurchase.objects.get(pk=pk, farm=farm)
        transaction = Transaction.objects.get(pk=request.data.get('transaction_id'))
        
        purchase.remove_transaction(transaction)
        serializer = EquipmentPurchaseSerializer(purchase)
        return Response(serializer.data)
    except (Farm.DoesNotExist, EquipmentPurchase.DoesNotExist, Transaction.DoesNotExist):
        return Response({"message": "Resource not found"}, status=404)

# Expense Categories Views
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_expense_categories(request, farm_id):
    """Get expense categories for specific farm"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        categories = Expense.EXPENSE_CATEGORIES
        return Response([{'value': cat[0], 'label': cat[1]} for cat in categories])
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_expense_category(request, farm_id):
    """Create new expense category (placeholder for future implementation)"""
    return Response({"message": "Expense categories are predefined"}, status=400)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def edit_expense_category(request, farm_id, pk):
    """Edit expense category (placeholder for future implementation)"""
    return Response({"message": "Expense categories are predefined"}, status=400)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def delete_expense_category(request, farm_id, pk):
    """Delete expense category (placeholder for future implementation)"""
    return Response({"message": "Expense categories are predefined"}, status=400)

# Farm Statistics Views
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_farm_statistics(request, farm_id):
    """Get farm statistics"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        
        # Calculate statistics
        total_income = Transaction.objects.filter(
            farm=farm, 
            transaction_type='incoming'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        total_expenses = Transaction.objects.filter(
            farm=farm, 
            transaction_type='outgoing'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        total_equipment = Equipment.objects.filter(farm=farm).count()
        total_expense_records = Expense.objects.filter(farm=farm).count()
        
        statistics = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_income': total_income - total_expenses,
            'total_equipment': total_equipment,
            'total_expense_records': total_expense_records,
            'farm_name': farm.name,
            'farm_id': farm.id
        }
        
        return Response(statistics)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_farm_income(request, farm_id):
    """Get farm income data"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        income_transactions = Transaction.objects.filter(
            farm=farm, 
            transaction_type='incoming'
        ).order_by('-transaction_date')
        
        serializer = TransactionSerializer(income_transactions, many=True)
        return Response(serializer.data)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_farm_expenses(request, farm_id):
    """Get farm expenses data"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        expense_transactions = Transaction.objects.filter(
            farm=farm, 
            transaction_type='outgoing'
        ).order_by('-transaction_date')
        
        serializer = TransactionSerializer(expense_transactions, many=True)
        return Response(serializer.data)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)

# Farm Users Views
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_farm_users(request, farm_id):
    """Get farm users (placeholder for future implementation)"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        # For now, return the farm owner
        users = [{
            'id': farm.created_by.id,
            'username': farm.created_by.username,
            'email': farm.created_by.email,
            'role': 'owner'
        }]
        return Response(users)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_farm_user(request, farm_id):
    """Add farm user (placeholder for future implementation)"""
    return Response({"message": "User management not implemented yet"}, status=400)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def remove_farm_user(request, farm_id, user_id):
    """Remove farm user (placeholder for future implementation)"""
    return Response({"message": "User management not implemented yet"}, status=400)

# Farm Settings Views
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_farm_settings(request, farm_id):
    """Get farm settings"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        settings = {
            'farm_id': farm.id,
            'name': farm.name,
            'address': farm.address,
            'phone': farm.phone,
            'coordinates': farm.coordinates,
            'size': farm.size,
            'size_unit': farm.size_unit,
            'description': farm.description,
            'code': farm.code,
            'image': farm.image,
            'image_reference': farm.image_refference
        }
        return Response(settings)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_farm_settings(request, farm_id):
    """Update farm settings"""
    try:
        farm = Farm.objects.get(id=farm_id, created_by=request.user)
        serializer = FarmSerializer(farm, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{farm_id} not found"}, status=404)
