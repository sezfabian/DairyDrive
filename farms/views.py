from django.contrib.auth.models import User
from users.functions import fix_phone_number
from .serializers import *
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
import random


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
