from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product, ProductionRecord, Buyer, Sale
from .serializers import ProductSerializer, ProductionRecordSerializer, BuyerSerializer, SaleSerializer
from farms.models import Farm
from animals.models import Animal, AnimalType

# Product Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_products(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    products = Product.objects.filter(farm=farm)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    product = get_object_or_404(Product, id=id, farm=farm)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    request.data["farm"] = farm_id

    # Check if product with same name already exists for this farm
    product_name = request.data.get('name')
    if product_name:
        existing_product = Product.objects.filter(
            farm=farm,
            name__iexact=product_name
        ).first()
        if existing_product:
            return Response(
                {'error': f'Product with name "{product_name}" already exists for this farm'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(farm=farm)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_product(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    request.data["farm"] = farm_id
    product = get_object_or_404(Product, id=id, farm=farm)
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save(farm=farm)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    product = get_object_or_404(Product, id=id, farm=farm)
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Production Record Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_production_records(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    animal_id = request.query_params.get('animal_id')
    animal_type_id = request.query_params.get('animal_type_id')
    product_id = request.query_params.get('product_id')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    records = ProductionRecord.objects.filter(farm=farm)
    
    if animal_id:
        records = records.filter(animal_id=animal_id)
    if animal_type_id:
        records = records.filter(animal_type_id=animal_type_id)
    if product_id:
        records = records.filter(product_id=product_id)
    if start_date:
        records = records.filter(date__gte=start_date)
    if end_date:
        records = records.filter(date__lte=end_date)

    serializer = ProductionRecordSerializer(records, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_production_record(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    record = get_object_or_404(ProductionRecord, id=id, farm=farm)
    serializer = ProductionRecordSerializer(record)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_production_record(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    request.data["farm"] = farm_id
    animal_id = request.data.get('animal')
    animal_type_id = request.data.get('animal_type')
    
    if animal_id:
        animal = get_object_or_404(Animal, id=animal_id, farm=farm)
        request.data['animal'] = animal.id
    elif animal_type_id:
        animal_type = get_object_or_404(AnimalType, id=animal_type_id)
        request.data['animal_type'] = animal_type.id
    
    serializer = ProductionRecordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(farm=farm)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_production_record(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    record = get_object_or_404(ProductionRecord, id=id, farm=farm)
    request.data["farm"] = farm_id
    animal_id = request.data.get('animal')
    animal_type_id = request.data.get('animal_type')
    
    if animal_id:
        animal = get_object_or_404(Animal, id=animal_id, farm=farm)
        request.data['animal'] = animal.id
    elif animal_type_id:
        animal_type = get_object_or_404(AnimalType, id=animal_type_id)
        request.data['animal_type'] = animal_type.id
    
    serializer = ProductionRecordSerializer(record, data=request.data)
    if serializer.is_valid():
        serializer.save(farm=farm)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_production_record(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    record = get_object_or_404(ProductionRecord, id=id, farm=farm)
    record.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Buyer Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_buyers(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    buyers = Buyer.objects.filter(farm=farm)
    serializer = BuyerSerializer(buyers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_buyer(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    buyer = get_object_or_404(Buyer, id=id, farm=farm)
    serializer = BuyerSerializer(buyer)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_buyer(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    request.data["farm"] = farm_id
    serializer = BuyerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(farm=farm)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_buyer(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    request.data["farm"] = farm_id
    buyer = get_object_or_404(Buyer, id=id, farm=farm)
    serializer = BuyerSerializer(buyer, data=request.data)
    if serializer.is_valid():
        serializer.save(farm=farm)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_buyer(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    buyer = get_object_or_404(Buyer, id=id, farm=farm)
    buyer.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Sale Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sales(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    buyer_id = request.query_params.get('buyer_id')
    product_id = request.query_params.get('product_id')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    payment_status = request.query_params.get('payment_status')

    sales = Sale.objects.filter(farm=farm)
    
    if buyer_id:
        sales = sales.filter(buyer_id=buyer_id)
    if product_id:
        sales = sales.filter(product_id=product_id)
    if start_date:
        sales = sales.filter(date__gte=start_date)
    if end_date:
        sales = sales.filter(date__lte=end_date)
    if payment_status is not None:
        sales = sales.filter(payment_status=payment_status.lower() == 'true')

    serializer = SaleSerializer(sales, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sale(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    sale = get_object_or_404(Sale, id=id, farm=farm)
    serializer = SaleSerializer(sale)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_sale(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    request.data["farm"] = farm_id
    buyer_id = request.data.get('buyer')
    buyer = get_object_or_404(Buyer, id=buyer_id, farm=farm)
    product_id = request.data.get('product')
    product = get_object_or_404(Product, id=product_id, farm=farm)
    
    serializer = SaleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(farm=farm, buyer=buyer, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_sale(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    sale = get_object_or_404(Sale, id=id, farm=farm)
    request.data["farm"] = farm_id
    buyer_id = request.data.get('buyer')
    buyer = get_object_or_404(Buyer, id=buyer_id, farm=farm)
    
    product_id = request.data.get('product')
    product = get_object_or_404(Product, id=product_id, farm=farm)
    
    serializer = SaleSerializer(sale, data=request.data)
    if serializer.is_valid():
        serializer.save(farm=farm, buyer=buyer, product=product)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_sale(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    sale = get_object_or_404(Sale, id=id, farm=farm)
    sale.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_sale_as_paid(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    sale = get_object_or_404(Sale, id=id, farm=farm)
    sale.payment_status = True
    sale.save()
    return Response({'status': 'payment marked as completed'})
