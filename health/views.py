from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Veterinarian, HealthCondition, VetService, HealthRecord, Treatment
from .serializers import (
    VeterinarianSerializer, HealthConditionSerializer, 
    VetServiceSerializer, HealthRecordSerializer, TreatmentSerializer
)
from farms.models import Farm
from animals.models import Animal

###################### VETERINARIANS ########################

@api_view(['GET'])
def get_veterinarians(request, farm_id):
    """Get veterinarians in a farm"""
    farm = Farm.objects.get(id=farm_id)
    veterinarians = Veterinarian.objects.filter(farm=farm)
    serializer = VeterinarianSerializer(veterinarians, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def add_veterinarian(request, farm_id):
    """Add veterinarian"""
    request.data["farm"] = farm_id
    serializer = VeterinarianSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def edit_veterinarian(request, id):
    """Edit veterinarian"""
    serializer = VeterinarianSerializer(data=request.data)
    if serializer.is_valid():
        veterinarian = Veterinarian.objects.get(id=id)
        for key, value in request.data.items():
            if key != "id":
                setattr(veterinarian, key, value)
        veterinarian.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def delete_veterinarian(request, id):
    """Delete veterinarian"""
    try:
        veterinarian = Veterinarian.objects.get(id=id)
        name = veterinarian.name
        veterinarian.delete()
        return Response({"message": f"Veterinarian id:{id} name:{name} deleted successfully"}, status=200)
    except Veterinarian.DoesNotExist:
        return Response({"error": f"Veterinarian with this id:{id} does not exist"}, status=400)

###################### HEALTH CONDITIONS ########################

@api_view(['GET'])
def get_health_conditions(request, farm_id):
    """Get health conditions in a farm"""
    farm = Farm.objects.get(id=farm_id)
    conditions = HealthCondition.objects.filter(farm=farm)
    serializer = HealthConditionSerializer(conditions, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def add_health_condition(request, farm_id):
    """Add health condition"""
    request.data["farm"] = farm_id
    serializer = HealthConditionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def edit_health_condition(request, id):
    """Edit health condition"""
    serializer = HealthConditionSerializer(data=request.data)
    if serializer.is_valid():
        condition = HealthCondition.objects.get(id=id)
        for key, value in request.data.items():
            if key != "id":
                setattr(condition, key, value)
        condition.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def delete_health_condition(request, id):
    """Delete health condition"""
    try:
        condition = HealthCondition.objects.get(id=id)
        name = condition.name
        condition.delete()
        return Response({"message": f"Health condition id:{id} name:{name} deleted successfully"}, status=200)
    except HealthCondition.DoesNotExist:
        return Response({"error": f"Health condition with this id:{id} does not exist"}, status=400)

###################### VET SERVICES ########################

@api_view(['GET'])
def get_vet_services(request, farm_id):
    """Get vet services in a farm"""
    farm = Farm.objects.get(id=farm_id)
    services = VetService.objects.filter(farm=farm)
    serializer = VetServiceSerializer(services, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def add_vet_service(request, farm_id):
    """Add vet service"""
    request.data["farm"] = farm_id
    serializer = VetServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def edit_vet_service(request, id):
    """Edit vet service"""
    serializer = VetServiceSerializer(data=request.data)
    if serializer.is_valid():
        service = VetService.objects.get(id=id)
        for key, value in request.data.items():
            if key != "id":
                setattr(service, key, value)
        service.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def delete_vet_service(request, id):
    """Delete vet service"""
    try:
        service = VetService.objects.get(id=id)
        name = service.name
        service.delete()
        return Response({"message": f"Vet service id:{id} name:{name} deleted successfully"}, status=200)
    except VetService.DoesNotExist:
        return Response({"error": f"Vet service with this id:{id} does not exist"}, status=400)

###################### HEALTH RECORDS ########################

@api_view(['GET'])
def get_health_records(request, farm_id):
    """Get health records for animals in a farm"""
    farm = Farm.objects.get(id=farm_id)
    animals = Animal.objects.filter(farm=farm)
    records = HealthRecord.objects.filter(animal__in=animals)
    
    # Filter by animal if specified
    if "animal" in request.query_params:
        animal_id = request.query_params["animal"]
        records = records.filter(animal_id=animal_id)
    
    # Filter by condition if specified
    if "condition" in request.query_params:
        condition_id = request.query_params["condition"]
        records = records.filter(condition_id=condition_id)
    
    # Filter by resolution status if specified
    if "is_resolved" in request.query_params:
        is_resolved = request.query_params["is_resolved"].lower() == "true"
        records = records.filter(is_resolved=is_resolved)
    
    serializer = HealthRecordSerializer(records, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_health_record(request, id):
    """Get specific health record"""
    try:
        record = HealthRecord.objects.get(id=id)
        serializer = HealthRecordSerializer(record)
        return Response(serializer.data, status=200)
    except HealthRecord.DoesNotExist:
        return Response({"error": f"Health record with id:{id} not found"}, status=404)

@api_view(['POST'])
def add_health_record(request):
    """Add health record"""
    serializer = HealthRecordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def edit_health_record(request, id):
    """Edit health record"""
    serializer = HealthRecordSerializer(data=request.data)
    if serializer.is_valid():
        record = HealthRecord.objects.get(id=id)
        for key, value in request.data.items():
            if key != "id":
                setattr(record, key, value)
        record.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def delete_health_record(request, id):
    """Delete health record"""
    try:
        record = HealthRecord.objects.get(id=id)
        record.delete()
        return Response({"message": f"Health record id:{id} deleted successfully"}, status=200)
    except HealthRecord.DoesNotExist:
        return Response({"error": f"Health record with this id:{id} does not exist"}, status=400)

###################### TREATMENTS ########################

@api_view(['GET'])
def get_treatments(request, health_record_id):
    """Get treatments for a health record"""
    treatments = Treatment.objects.filter(health_record_id=health_record_id)
    serializer = TreatmentSerializer(treatments, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def add_treatment(request):
    """Add treatment"""
    serializer = TreatmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def edit_treatment(request, id):
    """Edit treatment"""
    serializer = TreatmentSerializer(data=request.data)
    if serializer.is_valid():
        treatment = Treatment.objects.get(id=id)
        for key, value in request.data.items():
            if key != "id":
                setattr(treatment, key, value)
        treatment.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def delete_treatment(request, id):
    """Delete treatment"""
    try:
        treatment = Treatment.objects.get(id=id)
        treatment.delete()
        return Response({"message": f"Treatment id:{id} deleted successfully"}, status=200)
    except Treatment.DoesNotExist:
        return Response({"error": f"Treatment with this id:{id} does not exist"}, status=400)
