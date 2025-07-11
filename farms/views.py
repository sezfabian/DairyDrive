from django.contrib.auth.models import User
from users.functions import fix_phone_number
from .serializers import *
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
import random
from rest_framework import viewsets, permissions
from .models import Farm, Transaction, Equipment, Expense, EquipmentPurchase
from django.shortcuts import get_object_or_404


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

@api_view(['POST'])
def edit_farm(request, id):
    """Edit farm"""
    request.data["phone"] = fix_phone_number(request.data["phone"])
    request.data["created_by"] = request.user.id

    try:
        farm = Farm.objects.get(id=id)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{id} not found"}, status=404)
    
    # Ensure we're not creating a new farm with the same name
    if farm.name == request.data.get("name"):
        request.data.pop("name", None)

    serializer = FarmSerializer(farm, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def delete_farm(request, id):
    """Delete farm"""
    try:
        farm = Farm.objects.get(id=id)
        farm.delete()
        return Response({"message": f"Farm id:{id} deleted successfully"}, status=200)
    except Farm.DoesNotExist:
        return Response({"message": f"Farm id:{id} not found"}, status=404)

# Transaction specific views
@api_view(['GET'])
def get_transactions(request):
    """Get all transactions"""
    transactions = Transaction.objects.filter(farm__created_by=request.user)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def create_transaction(request):
    """Create a new transaction"""
    request.data["created_by"] = request.user.id
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def edit_transaction(request, pk):
    """Edit an existing transaction"""
    try:
        transaction = Transaction.objects.get(pk=pk, farm__created_by=request.user)
    except Transaction.DoesNotExist:
        return Response({"message": f"Transaction id:{pk} not found"}, status=404)

    serializer = TransactionSerializer(transaction, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def delete_transaction(request, pk):
    """Delete a transaction"""
    try:
        transaction = Transaction.objects.get(pk=pk, farm__created_by=request.user)
        transaction.delete()
        return Response({"message": f"Transaction id:{pk} deleted successfully"}, status=200)
    except Transaction.DoesNotExist:
        return Response({"message": f"Transaction id:{pk} not found"}, status=404)

@api_view(['GET'])
def get_transaction(request, pk):
    """Get a specific transaction"""
    try:
        transaction = Transaction.objects.get(pk=pk, farm__created_by=request.user)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=200)
    except Transaction.DoesNotExist:
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
def get_equipment(request):
    """Get all equipment for user's farms"""
    equipment = Equipment.objects.filter(farm__created_by=request.user)
    serializer = EquipmentSerializer(equipment, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_equipment(request):
    """Create new equipment"""
    request.data['created_by'] = request.user.id
    serializer = EquipmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def edit_equipment(request, pk):
    """Edit existing equipment"""
    equipment = get_object_or_404(Equipment, pk=pk, farm__created_by=request.user)
    serializer = EquipmentSerializer(equipment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def delete_equipment(request, pk):
    """Delete equipment"""
    equipment = get_object_or_404(Equipment, pk=pk, farm__created_by=request.user)
    equipment.delete()
    return Response(status=204)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_equipment_detail(request, pk):
    """Get specific equipment details"""
    equipment = get_object_or_404(Equipment, pk=pk, farm__created_by=request.user)
    serializer = EquipmentSerializer(equipment)
    return Response(serializer.data)

# Expense Views
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_expenses(request):
    """Get all expenses for user's farms"""
    expenses = Expense.objects.filter(farm__created_by=request.user)
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_expense(request):
    """Create new expense"""
    request.data['created_by'] = request.user.id
    serializer = ExpenseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def edit_expense(request, pk):
    """Edit existing expense"""
    expense = get_object_or_404(Expense, pk=pk, farm__created_by=request.user)
    serializer = ExpenseSerializer(expense, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def delete_expense(request, pk):
    """Delete expense"""
    expense = get_object_or_404(Expense, pk=pk, farm__created_by=request.user)
    expense.delete()
    return Response(status=204)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_expense_detail(request, pk):
    """Get specific expense details"""
    expense = get_object_or_404(Expense, pk=pk, farm__created_by=request.user)
    serializer = ExpenseSerializer(expense)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_expense_transaction(request, pk):
    """Add a transaction to an expense"""
    expense = get_object_or_404(Expense, pk=pk, farm__created_by=request.user)
    transaction = get_object_or_404(Transaction, pk=request.data.get('transaction_id'))
    
    if transaction.farm != expense.farm:
        return Response({"error": "Transaction must be from the same farm"}, status=400)
    
    expense.add_transaction(transaction)
    serializer = ExpenseSerializer(expense)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def remove_expense_transaction(request, pk):
    """Remove a transaction from an expense"""
    expense = get_object_or_404(Expense, pk=pk, farm__created_by=request.user)
    transaction = get_object_or_404(Transaction, pk=request.data.get('transaction_id'))
    
    expense.remove_transaction(transaction)
    serializer = ExpenseSerializer(expense)
    return Response(serializer.data)

# Equipment Purchase Views
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_equipment_purchases(request):
    """Get all equipment purchases for user's farms"""
    purchases = EquipmentPurchase.objects.filter(farm__created_by=request.user)
    serializer = EquipmentPurchaseSerializer(purchases, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_equipment_purchase(request):
    """Create new equipment purchase"""
    request.data['created_by'] = request.user.id
    serializer = EquipmentPurchaseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def edit_equipment_purchase(request, pk):
    """Edit existing equipment purchase"""
    purchase = get_object_or_404(EquipmentPurchase, pk=pk, farm__created_by=request.user)
    serializer = EquipmentPurchaseSerializer(purchase, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def delete_equipment_purchase(request, pk):
    """Delete equipment purchase"""
    purchase = get_object_or_404(EquipmentPurchase, pk=pk, farm__created_by=request.user)
    purchase.delete()
    return Response(status=204)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_equipment_purchase_detail(request, pk):
    """Get specific equipment purchase details"""
    purchase = get_object_or_404(EquipmentPurchase, pk=pk, farm__created_by=request.user)
    serializer = EquipmentPurchaseSerializer(purchase)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_equipment_purchase_transaction(request, pk):
    """Add a transaction to an equipment purchase"""
    purchase = get_object_or_404(EquipmentPurchase, pk=pk, farm__created_by=request.user)
    transaction = get_object_or_404(Transaction, pk=request.data.get('transaction_id'))
    
    if transaction.farm != purchase.farm:
        return Response({"error": "Transaction must be from the same farm"}, status=400)
    
    purchase.add_transaction(transaction)
    serializer = EquipmentPurchaseSerializer(purchase)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def remove_equipment_purchase_transaction(request, pk):
    """Remove a transaction from an equipment purchase"""
    purchase = get_object_or_404(EquipmentPurchase, pk=pk, farm__created_by=request.user)
    transaction = get_object_or_404(Transaction, pk=request.data.get('transaction_id'))
    
    purchase.remove_transaction(transaction)
    serializer = EquipmentPurchaseSerializer(purchase)
    return Response(serializer.data)
