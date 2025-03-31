from django.contrib.auth.models import User
from .serializers import *
from farms.models import Farm
from datetime import date
from users.models import UserProfile
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response


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
def edit_animal_type(request, id):
    """Edit animal type"""
    serializer = AnimalTypeSerializer(data=request.data)
    if serializer.is_valid():
        animal_type = AnimalType.objects.get(id=id)
        for key, value in request.data.items():
            if key != "id":
                setattr(animal_type, key, value)
        animal_type.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def delete_animal_type(request, id):
    """Delete animal type"""
    try:
        animal_type = AnimalType.objects.get(id=id)
        name = animal_type.name
        animal_type.delete()
        return Response({"message": f"Animal type id:{id} name:{name} deleted successfully"}, status=200)
    except AnimalType.DoesNotExist:
        return Response({"error": f"Animal type with this id:{id} does not exist"}, status=400)

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
def edit_animal_breed(request, id):
    """Edit animal breed"""
    serializer = AnimalBreedSerializer(data=request.data)
    if serializer.is_valid():
        animal_breed = AnimalBreed.objects.get(id=id)
        for key, value in request.data.items():
            if key != "id":
                setattr(animal_breed, key, value)
        animal_breed.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def delete_animal_breed(request, id):
    """Delete animal breed"""
    try:
        animal_breed = AnimalBreed.objects.get(id=id)
        name = animal_breed.name
        animal_breed.delete()
        return Response({"message": f"Animal breed id:{id} name:{name} deleted successfully"}, status=200)
    except AnimalBreed.DoesNotExist:
        return Response({"error": f"Animal breed with this id:{id} does not exist"}, status=400)


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
    serializer = AnimalSerializer(animals, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_animal(request, id):
    """Get animal"""
    try:
        animal = Animal.objects.get(id=id)
        serializer = AnimalSerializer(animal)
        return Response(serializer.data, status=200)
    except Animal.DoesNotExist:
        return Response({"message": f"Animal id:{id} not found"}, status=404)

@api_view(['POST'])
def create_animal(request, farm_id):
    """Create animal"""
    request.data["farm"] = farm_id
    request.data["created_by"] = request.user.id
    serializer = AnimalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def edit_animal(request, id):
    """Edit animal"""
    request.data["created_by"] = request.user.id
    try:
        animal = Animal.objects.get(id=id)
        for key, value in request.data.items():
            if key == "type":
                animal_type = AnimalType.objects.get(id=value)
                setattr(animal, key, animal_type)
            elif key == "breed":
                animal_breed = AnimalBreed.objects.get(id=value)
                setattr(animal, key, animal_breed)
            elif key == "farm":
                farm = Farm.objects.get(id=value)
                setattr(animal, key, farm)
            elif key != "id" and key != "created_by":
                setattr(animal, key, value)
        animal.save()
        serializer = AnimalSerializer(animal)
        return Response(serializer.data, status=200)
    except Animal.DoesNotExist:
        return Response({"error": f"Animal with this id:{id} does not exist"}, status=400)
    except KeyError:
        return Response({"error": "Invalid data"}, status=400)

    return Response(serializer.errors, status=400)

@api_view(['POST'])
def delete_animal(request, id):
    """Delete animal"""
    try:
        animal = Animal.objects.get(id=id)
        name = animal.name
        animal.delete()
        return Response({"message": f"Animal id:{id} name:{name} deleted successfully"}, status=200)
    except Animal.DoesNotExist:
        return Response({"error": f"Animal with this id:{id} does not exist"}, status=400)

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

@api_view(['POST'])
def delete_animal_image(request, id):
    """Delete animal image"""
    try:
        animal_image = AnimalImage.objects.get(id=id)
        animal_image.delete()
        return Response({"message": f"Animal image id:{id} deleted successfully"}, status=200)
    except AnimalImage.DoesNotExist:
        return Response({"error": f"Animal image with this id:{id} does not exist"}, status=400)

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
    serializer = ArtificialInseminationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def edit_ai_record(request, id):
    """Edit AI record"""
    serializer = ArtificialInseminationSerializer(data=request.data)
    if serializer.is_valid():
        ai_record = ArtificialInsemination.objects.get(id=id)
        for key, value in request.data.items():
            if key != "id":
                setattr(ai_record, key, value)
        ai_record.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def delete_ai_record(request, id):
    """Delete AI record"""
    try:
        ai_record = ArtificialInsemination.objects.get(id=id)
        ai_record.delete()
        return Response({"message": f"AI record id:{id} deleted successfully"}, status=200)
    except ArtificialInsemination.DoesNotExist:
        return Response({"error": f"AI record with this id:{id} does not exist"}, status=400)

@api_view(['POST'])
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

@api_view(['POST'])
def clear_ai_sire(request, animal_id):
    """Clear AI sire for an animal"""
    try:
        animal = Animal.objects.get(id=animal_id)
        animal.ai_sire = None
        animal.save()
        return Response({"message": f"AI sire cleared successfully for animal {animal.name}"}, status=200)
    except Animal.DoesNotExist:
        return Response({"error": f"Animal with id:{animal_id} does not exist"}, status=400)