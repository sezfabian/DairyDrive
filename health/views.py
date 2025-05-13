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

@api_view(['GET'])
def get_veterinarian(request, farm_id, id):
    """Get specific veterinarian"""
    try:
        veterinarian = Veterinarian.objects.get(id=id, farm_id=farm_id)
        serializer = VeterinarianSerializer(veterinarian)
        return Response(serializer.data, status=200)
    except Veterinarian.DoesNotExist:
        return Response({"error": f"Veterinarian with id:{id} not found in farm:{farm_id}"}, status=404)


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
def edit_veterinarian(request, farm_id, id):
    """Edit veterinarian"""
    try:
        veterinarian = Veterinarian.objects.get(id=id, farm_id=farm_id)
        serializer = VeterinarianSerializer(veterinarian, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    except Veterinarian.DoesNotExist:
        return Response({"error": f"Veterinarian with id:{id} not found in farm:{farm_id}"}, status=404)

@api_view(['POST'])
def delete_veterinarian(request, farm_id, id):
    """Delete veterinarian"""
    try:
        veterinarian = Veterinarian.objects.get(id=id, farm_id=farm_id)
        veterinarian.delete()
        return Response({"message": "Veterinarian deleted successfully"}, status=200)
    except Veterinarian.DoesNotExist:
        return Response({"error": f"Veterinarian with id:{id} not found in farm:{farm_id}"}, status=404)

###################### HEALTH CONDITIONS ########################

@api_view(['GET'])
def get_health_conditions(request, farm_id):
    """Get health conditions in a farm"""
    farm = Farm.objects.get(id=farm_id)
    conditions = HealthCondition.objects.filter(farm=farm)
    serializer = HealthConditionSerializer(conditions, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_health_condition(request, farm_id, id):
    """Get specific health condition"""
    try:
        condition = HealthCondition.objects.get(id=id, farm_id=farm_id)
        serializer = HealthConditionSerializer(condition)
        return Response(serializer.data, status=200)
    except HealthCondition.DoesNotExist:
        return Response({"error": f"Health condition with id:{id} not found in farm:{farm_id}"}, status=404)

@api_view(['POST'])
def add_health_condition(request, farm_id):
    """Add health condition"""
    request.data["farm"] = farm_id
    serializer = HealthConditionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def edit_health_condition(request, farm_id, id):
    """Edit health condition"""
    try:
        condition = HealthCondition.objects.get(id=id, farm_id=farm_id)
        serializer = HealthConditionSerializer(condition, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    except HealthCondition.DoesNotExist:
        return Response({"error": f"Health condition with id:{id} not found in farm:{farm_id}"}, status=404)

@api_view(['DELETE'])
def delete_health_condition(request, farm_id, id):
    """Delete health condition"""
    try:
        condition = HealthCondition.objects.get(id=id, farm_id=farm_id)
        condition.delete()
        return Response({"message": "Health condition deleted successfully"}, status=200)
    except HealthCondition.DoesNotExist:
        return Response({"error": f"Health condition with id:{id} not found in this farm"}, status=404)

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

@api_view(['PUT'])
def edit_vet_service(request, id, farm_id):
    """Edit vet service"""
    try:
        service = VetService.objects.get(id=id, farm_id=farm_id)
        serializer = VetServiceSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    except VetService.DoesNotExist:
        return Response({"error": f"Vet service with id:{id} not found in farm:{farm_id}"}, status=404)

@api_view(['DELETE'])
def delete_vet_service(request, id, farm_id):
    """Delete vet service"""
    try:
        service = VetService.objects.get(id=id, farm_id=farm_id)
        service.delete()
        return Response({"message": "Vet service deleted successfully"}, status=200)
    except VetService.DoesNotExist:
        return Response({"error": f"Vet service with id:{id} not found in farm:{farm_id}"}, status=404)

@api_view(['GET'])
def get_vet_service(request, farm_id, id):
    """Get specific vet service"""
    try:
        service = VetService.objects.get(id=id, farm_id=farm_id)
        serializer = VetServiceSerializer(service)
        return Response(serializer.data, status=200)
    except VetService.DoesNotExist:
        return Response({"error": f"Vet service with id:{id} not found in farm:{farm_id}"}, status=404)

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
def get_health_record(request, farm_id, id):
    """Get specific health record"""
    try:
        record = HealthRecord.objects.get(id=id, animal__farm_id=farm_id)
        serializer = HealthRecordSerializer(record)
        return Response(serializer.data, status=200)
    except HealthRecord.DoesNotExist:
        return Response({"error": f"Health record with id:{id} not found in farm:{farm_id}"}, status=404)

@api_view(['POST'])
def add_health_record(request):
    """Add health record"""
    serializer = HealthRecordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def edit_health_record(request, farm_id, id):
    """Edit health record"""
    try:
        record = HealthRecord.objects.get(id=id, animal__farm_id=farm_id)
        serializer = HealthRecordSerializer(record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    except HealthRecord.DoesNotExist:
        return Response({"error": f"Health record with id:{id} not found in farm:{farm_id}"}, status=404)

@api_view(['DELETE'])
def delete_health_record(request, farm_id, id):
    """Delete health record"""
    try:
        record = HealthRecord.objects.get(id=id, animal__farm_id=farm_id)
        record.delete()
        return Response({"message": "Health record deleted successfully"}, status=200)
    except HealthRecord.DoesNotExist:
        return Response({"error": f"Health record with id:{id} not found in farm:{farm_id}"}, status=404)

###################### TREATMENTS ########################

@api_view(['GET'])
def get_treatments(request, farm_id):
    """Get treatments for a farm"""
    treatments = Treatment.objects.filter(health_record__animal__farm_id=farm_id)
    serializer = TreatmentSerializer(treatments, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_treatments_by_health_record(request, health_record_id):
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

@api_view(['PUT'])
def edit_treatment(request, farm_id, id):
    """Edit treatment"""
    try:
        treatment = Treatment.objects.get(id=id, health_record__animal__farm_id=farm_id)
        serializer = TreatmentSerializer(treatment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    except Treatment.DoesNotExist:
        return Response({"error": f"Treatment with id:{id} not found in farm:{farm_id}"}, status=404)

@api_view(['DELETE'])
def delete_treatment(request, farm_id, id):
    """Delete treatment"""
    try:
        treatment = Treatment.objects.get(id=id, health_record__animal__farm_id=farm_id)
        treatment.delete()
        return Response({"message": "Treatment deleted successfully"}, status=200)
    except Treatment.DoesNotExist:
        return Response({"error": f"Treatment with id:{id} not found in farm:{farm_id}"}, status=404)

@api_view(['GET'])
def get_treatment(request, farm_id, id):
    """Get specific treatment"""
    try:
        treatment = Treatment.objects.get(id=id, health_record__animal__farm_id=farm_id)
        serializer = TreatmentSerializer(treatment)
        return Response(serializer.data, status=200)
    except Treatment.DoesNotExist:
        return Response({"error": f"Treatment with id:{id} not found in farm:{farm_id}"}, status=404)
