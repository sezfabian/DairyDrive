from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from .functions import fix_phone_number
from .serializers import *
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
from farms.models import Farm


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    #Fix phone number
    request.data["phone"] = fix_phone_number(request.data["phone"])

    # Check if user already exists
    if User.objects.filter(email=request.data["email"]).exists():
        return Response({"error": "User with this email already exists"}, status=400)
    # Create user
    user = User.objects.create_user(username=request.data["email"], password=request.data["password"], email=request.data["email"])
    user.save()
    # Create user profile
    request.data["user"] = user.id
    serializer = UserProfileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        # Login user
        user = authenticate(request, username=serializer.data["email"], password=request.data["password"])
        refresh = RefreshToken.for_user(user)
        # Return access, refresh token and user profile
        return Response({"refresh": str(refresh), "access": str(refresh.access_token), "profile": serializer.data}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):
    # Check Farm Code
    if "farm_code" in request.data:
        try:
            farm = Farm.objects.get(code=request.data["farm_code"].upper())
        except Farm.DoesNotExist:
            return Response({"error": "Farm with this code does not exist"}, status=400)
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        # Check if email or phone number
        try:
            if "@" in request.data["email_or_phone"]:
                profile = UserProfile.objects.get(email=request.data["email_or_phone"])
            else:
                profile = UserProfile.objects.get(phone=request.data["email_or_phone"])
        except UserProfile.DoesNotExist:
            return Response({"error": "User with this email or phone number does not exist"}, status=400)
        email = profile.email


        # Check if user has acces to farm
        if farm:
            if farm.id in profile.farms.all().values_list('id', flat=True):
                pass
            else:
                return Response({"error": "User does not have access to this farm"}, status=400)

        # Login user
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=email, password=serializer.data["password"])
            refresh = RefreshToken.for_user(user)
            serializer = UserProfileSerializer(profile)
            # Return access, refresh token, farm id and user profile
            return Response({"refresh": str(refresh), "access": str(refresh.access_token), "farm": farm.id, "profile": serializer.data}, status=200)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=400)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def logout(request):
    """Logout user"""
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token

        return Response({"success": "Logged out successfully"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
def get_profile(request):
    """Get user profile"""
    profile = UserProfile.objects.get(user=request.user)
    serializer = UserProfileSerializer(profile)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def edit_profile(request):
    """Update user profile"""
    profile = UserProfile.objects.get(user=request.user)
    serializer = UserProfileSerializer(profile, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)