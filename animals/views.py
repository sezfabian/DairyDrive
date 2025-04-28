from django.contrib.auth.models import User
from .serializers import *
from farms.models import Farm
from datetime import date
from users.models import UserProfile
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
from health.models import HealthRecord


###################### ANIMAL TYPES ########################
@api_view(['GET'])
def get_animal_types(request, farm_id):
    """Get animal types in a farm"""
    farm = Farm.objects.get(id=farm_id)
    animal_types = AnimalType.objects.filter(farm=farm)
    serializer = AnimalTypeSerializer(animal_types, many=True)
    return Response(serializer.data, status=200)


@api_view(['POST'])
def add_animal_type(request, farm_id):
    """Add animal type"""
    request.data["farm"] = farm_id
    request.data["created_by"] = request.user.id
    serializer = AnimalTypeSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data["name"] in [type.name for type in AnimalType.objects.filter(farm=farm_id)]:
            return Response({"error": "Animal type with this name already exists"}, status=400)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def edit_animal_type(request, farm_id, id):
    """Edit animal type"""
    try:
        animal_type = AnimalType.objects.get(id=id, farm_id=farm_id)
        serializer = AnimalTypeSerializer(animal_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    except AnimalType.DoesNotExist:
        return Response({"error": f"Animal type with id:{id} not found in farm:{farm_id}"}, status=404)

@api_view(['POST'])
def delete_animal_type(request, farm_id, id):
    """Delete animal type"""
    try:
        animal_type = AnimalType.objects.get(id=id, farm_id=farm_id)
        animal_type.delete()
        return Response({"message": "Animal type deleted successfully"}, status=200)
    except AnimalType.DoesNotExist:
        return Response({"error": f"Animal type with id:{id} not found in farm:{farm_id}"}, status=404)

###################### ANIMAL BREEDS ########################

@api_view(['GET'])
def get_animal_breeds(request, farm_id):
    """Get animal breeds"""
    farm = Farm.objects.get(id=farm_id)
    animal_breeds = AnimalBreed.objects.filter(farm=farm)
    serializer = AnimalBreedSerializer(animal_breeds, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_animal_breeds_by_type(request, id):
    try:
        animal_type = AnimalType.objects.get(id=id)
        animal_breeds = AnimalBreed.objects.filter(type=animal_type)
        serializer = AnimalBreedSerializer(animal_breeds, many=True)
        return Response(serializer.data, status=200)
    except AnimalType.DoesNotExist:
        return Response({"error": f"Animal type with this id:{id} does not exist"}, status=400)

@api_view(['POST'])
def add_animal_breed(request, farm_id):
    """Add animal breed"""
    request.data["farm"] = farm_id
    serializer = AnimalBreedSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def edit_animal_breed(request, farm_id, id):
    """Edit animal breed"""
    try:
        animal_breed = AnimalBreed.objects.get(id=id, farm_id=farm_id)
        serializer = AnimalBreedSerializer(animal_breed, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    except AnimalBreed.DoesNotExist:
        return Response({"error": f"Animal breed with id:{id} not found in farm:{farm_id}"}, status=404)

@api_view(['POST'])
def delete_animal_breed(request, farm_id, id):
    """Delete animal breed"""
    try:
        animal_breed = AnimalBreed.objects.get(id=id, farm_id=farm_id)
        animal_breed.delete()
        return Response({"message": "Animal breed deleted successfully"}, status=200)
    except AnimalBreed.DoesNotExist:
        return Response({"error": f"Animal breed with id:{id} not found in farm:{farm_id}"}, status=404)


###################### ANIMALS ########################

@api_view(['GET'])
def get_animals(request, farm_id):
    """Get animals, Returns animals in users farms"""
    farm = Farm.objects.get(id=farm_id)
    animals = Animal.objects.filter(farm=farm)
    # if breed is specified
    if "breed" in request.query_params:
        breed = request.query_params["breed"]
        animals = animals.filter(breed__name=breed)

    # if name is specified
    if "name" in request.query_params:
        name = request.query_params["name"]
        animals = animals.filter(name__icontains=name)

    # if type is specified
    if "type" in request.query_params:
        type = request.query_params["type"]
        animals = animals.filter(type__name=type)
    # Serialize the animal data
    serializer = AnimalSerializer(animals, many=True, context={'many': True})
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_animal(request, farm_id, id):
    """Get specific animal"""
    try:
        animal = Animal.objects.get(id=id, farm_id=farm_id)
        serializer = AnimalSerializer(animal, context={'many': False})
        return Response(serializer.data, status=200)
    except Animal.DoesNotExist:
        return Response({"error": f"Animal with id:{id} not found in farm:{farm_id}"}, status=404)

@api_view(['POST'])
def add_animal(request, farm_id):
    """Add animal"""
    request.data["farm"] = farm_id
    request.data["created_by"] = request.user.id
    serializer = AnimalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def edit_animal(request, farm_id, id):
    """Edit animal"""
    try:
        animal = Animal.objects.get(id=id, farm_id=farm_id)
        serializer = AnimalSerializer(animal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    except Animal.DoesNotExist:
        return Response({"error": f"Animal with id:{id} not found in farm:{farm_id}"}, status=404)

@api_view(['DELETE'])
def delete_animal(request, farm_id, id):
    """Delete animal"""
    try:
        animal = Animal.objects.get(id=id, farm_id=farm_id)
        animal.delete()
        return Response({"message": "Animal deleted successfully"}, status=200)
    except Animal.DoesNotExist:
        return Response({"error": f"Animal with id:{id} not found in farm:{farm_id}"}, status=404)

@api_view(['POST'])
def post_animal_image(request, id):
    """Post animal image"""
    try:
        animal = Animal.objects.get(id=id)
        request.data["animal"] = id
        serializer = AnimalImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(animal=animal)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    except Animal.DoesNotExist:
        return Response({"error": f"Animal with this id:{id} does not exist"}, status=400)

@api_view(['DELETE'])
def delete_animal_image(request, farm_id, id):
    """Delete animal image"""
    try:
        animal_image = AnimalImage.objects.get(id=id, animal__farm_id=farm_id)
        animal_image.delete()
        return Response({"message": "Animal image deleted successfully"}, status=200)
    except AnimalImage.DoesNotExist:
        return Response({"error": f"Animal image with id:{id} not found in farm:{farm_id}"}, status=404)

###################### ARTIFICIAL INSEMINATION ########################

@api_view(['GET'])
def get_ai_records(request, farm_id):
    """Get AI records in a farm"""
    farm = Farm.objects.get(id=farm_id)
    ai_records = ArtificialInsemination.objects.filter(farm=farm)
    
    # Filter by animal if specified
    if "animal" in request.query_params:
        animal_id = request.query_params["animal"]
        ai_records = ai_records.filter(animal_id=animal_id)
    
    # Filter by status if specified
    if "status" in request.query_params:
        status = request.query_params["status"]
        ai_records = ai_records.filter(status=status)
    
    serializer = ArtificialInseminationSerializer(ai_records, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def add_ai_record(request, farm_id):
    """Add AI record"""
    request.data["farm"] = farm_id
    request.data["created_by"] = request.user.id
    
    # Validate that the animal exists and is female
    try:
        animal_id = request.data.get('animal')
        if not animal_id:
            return Response({"error": "Animal ID is required"}, status=400)
            
        animal = Animal.objects.get(id=animal_id, farm_id=farm_id)
        if animal.gender != 'Female':
            return Response({"error": "AI can only be performed on female animals"}, status=400)
    except Animal.DoesNotExist:
        return Response({"error": f"Animal with id:{animal_id} not found in farm:{farm_id}"}, status=404)
    
    serializer = ArtificialInseminationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def edit_ai_record(request, farm_id, id):
    """Edit AI record"""
    try:
        ai_record = ArtificialInsemination.objects.get(id=id, animal__farm_id=farm_id)
        serializer = ArtificialInseminationSerializer(ai_record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    except ArtificialInsemination.DoesNotExist:
        return Response({"error": f"AI record with id:{id} not found in farm:{farm_id}"}, status=404)

@api_view(['DELETE'])
def delete_ai_record(request, farm_id, id):
    """Delete AI record"""
    try:
        ai_record = ArtificialInsemination.objects.get(id=id, animal__farm_id=farm_id)
        ai_record.delete()
        return Response({"message": "AI record deleted successfully"}, status=200)
    except ArtificialInsemination.DoesNotExist:
        return Response({"error": f"AI record with id:{id} not found in farm:{farm_id}"}, status=404)

@api_view(['PUT'])
def set_ai_sire(request, animal_id):
    """Set AI sire for an animal"""
    try:
        animal = Animal.objects.get(id=animal_id)
        ai_record_id = request.data.get('ai_record_id')
        
        if not ai_record_id:
            return Response({"error": "AI record ID is required"}, status=400)
            
        try:
            ai_record = ArtificialInsemination.objects.get(id=ai_record_id)
            if ai_record.animal != animal:
                return Response({"error": "AI record does not belong to this animal"}, status=400)
            if ai_record.status != 'SUCCESSFUL':
                return Response({"error": "Only successful AI records can be set as sire"}, status=400)
                
            animal.ai_sire = ai_record
            animal.sire = None  # Clear natural sire if exists
            animal.save()
            
            return Response({"message": f"AI sire set successfully for animal {animal.name}"}, status=200)
        except ArtificialInsemination.DoesNotExist:
            return Response({"error": f"AI record with id:{ai_record_id} does not exist"}, status=400)
            
    except Animal.DoesNotExist:
        return Response({"error": f"Animal with id:{animal_id} does not exist"}, status=400)

@api_view(['PUT'])
def clear_ai_sire(request, animal_id):
    """Clear AI sire for an animal"""
    try:
        animal = Animal.objects.get(id=animal_id)
        animal.ai_sire = None
        animal.save()
        return Response({"message": f"AI sire cleared successfully for animal {animal.name}"}, status=200)
    except Animal.DoesNotExist:
        return Response({"error": f"Animal with id:{animal_id} does not exist"}, status=400)

@api_view(['GET'])
def get_animal_health_records(request, animal_id):
    """Get health records for a specific animal"""
    try:
        animal = Animal.objects.get(id=animal_id)
        health_records = HealthRecord.objects.filter(animal=animal).order_by('-diagnosis_date')
        serializer = HealthRecordSerializer(health_records, many=True)
        return Response(serializer.data, status=200)
    except Animal.DoesNotExist:
        return Response({"error": f"Animal with id:{animal_id} does not exist"}, status=404)