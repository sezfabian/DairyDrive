from django.contrib.auth.models import User
from .serializers import *
from farms.models import Farm
from datetime import date
from users.models import UserProfile
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response


###################### ANIMAL TYPES ########################
@api_view(['GET'])
def get_animal_types(request):
    """Get animal types"""
    animal_types = AnimalType.objects.all()
    serializer = AnimalTypeSerializer(animal_types, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def add_animal_type(request):
    """Add animal type"""
    serializer = AnimalTypeSerializer(data=request.data)
    if serializer.is_valid():
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
def get_animal_breeds(request):
    """Get animal breeds"""
    animal_breeds = AnimalBreed.objects.all()
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
def add_animal_breed(request):
    """Add animal breed"""
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
def get_animals(request):
    """Get animals, Returns animals in users farms"""
    # Get the user's profile
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    # Get the farms associated with the user
    farms = user_profile.farms.all()
    # Get animals in the user's farms
    animals = Animal.objects.filter(farm__in=farms)

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
def create_animal(request):
    """Create animal"""
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