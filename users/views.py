from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile, SubscriptionPlan, UserSubscription, PaymentHistory
from .functions import fix_phone_number
from .serializers import *
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
from farms.models import Farm
from animals.models import Animal, AnimalType, AnimalBreed
from animals.serializers import AnimalSerializer, AnimalTypeSerializer, AnimalBreedSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import stripe
from .decorators import require_feature
from datetime import datetime, timedelta

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    #Fix phone number
    request.data["phone"] = fix_phone_number(request.data["phone"])

    # Check if farm code is valid
    if "farm_code" in request.data:
        if Farm.objects.filter(code=request.data["farm_code"].upper()).exists():
            farm = Farm.objects.get(code=request.data["farm_code"].upper())
            farm_details = FarmSerializer(farm).data
            farm_details["id"] = farm.id
        elif request.data["farm_code"].upper() == "":
            pass
        else:
            return Response({"error": "The farm code you have entered is not valid"}, status=400)

    # Check if user already exists
    if User.objects.filter(email=request.data["email"]).exists():
        return Response({"error": "User with this email already exists"}, status=400)
    if  UserProfile.objects.filter(phone=request.data["phone"]).exists():
        return Response({"error": "User with this phone number already exists"}, status=400)
    
    # Create user
    user = User.objects.create_user(username=request.data["email"], password=request.data["password"], email=request.data["email"])
    user.save()
    # Create user profile
    request.data["user"] = user.id
    serializer = UserProfileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        # Get user profile
        user_profile = UserProfile.objects.get(email=request.data["email"])
        if "farm_code" in request.data:
            user_profile.farms.add(farm)
            user_profile.save()
        user_profile = UserProfileSerializer(user_profile).data
        # Login user
        user = authenticate(request, username=serializer.data["email"], password=request.data["password"])
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        # Calculate token expiration time
        expires_in = int((access_token.current_time + access_token.lifetime - access_token.current_time).total_seconds())
        
        # Return access, refresh token, expiration time and user profile
        return Response({
            "refresh": str(refresh),
            "access": str(access_token),
            "expires_in": expires_in,
            "farm": farm_details if "farm_code" in request.data else None,
            "profile": user_profile
        }, status=201)
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
        if "farm_code" in request.data:
            if farm.id in profile.farms.all().values_list('id', flat=True):
                farm_details = FarmSerializer(farm)
                animals = Animal.objects.filter(farm=farm)
                types = AnimalType.objects.filter(farm=farm)
                breeds = AnimalBreed.objects.filter(farm=farm)
            else:
                return Response({"error": "User does not have access to this farm"}, status=400)

            farm_details = farm_details.data
            farm_details["id"] = farm.id
            farm_details["animals"] = AnimalSerializer(animals, many=True).data
            farm_details["types"] = AnimalTypeSerializer(types, many=True).data
            farm_details["breeds"] = AnimalBreedSerializer(breeds, many=True).data

        # Login user
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=email, password=serializer.data["password"])
            if not user:
                return Response({"error": "Your email or password is Invalid"}, status=400)
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            # Calculate token expiration time
            expires_in = int((access_token.current_time + access_token.lifetime - access_token.current_time).total_seconds())
            
            serializer = UserProfileSerializer(profile)
            # Return access, refresh token, expiration time, farm id and user profile
            return Response({
                "refresh": str(refresh),
                "access": str(access_token),
                "expires_in": expires_in,
                "farm": farm_details if "farm_code" in request.data else None,
                "profile": serializer.data
            }, status=200)
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

@api_view(['GET'])
def get_farm(request, farm_id):
    """Get farm"""
    farm = Farm.objects.get(id=farm_id)
    animals = Animal.objects.filter(farm=farm)
    types = AnimalType.objects.filter(farm=farm)
    breeds = AnimalBreed.objects.filter(farm=farm)

    farm_details = FarmSerializer(farm)
    farm_details = farm_details.data
    farm_details["id"] = farm.id
    farm_details["animals"] = AnimalSerializer(animals, many=True).data
    farm_details["types"] = AnimalTypeSerializer(types, many=True).data
    farm_details["breeds"] = AnimalBreedSerializer(breeds, many=True).data

    return Response(farm_details, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subscription_plans(request):
    """Get available subscription plans"""
    plans = SubscriptionPlan.objects.all()
    return Response([{
        'id': plan.id,
        'name': plan.name,
        'description': plan.description,
        'price': plan.price,
        'duration_days': plan.duration_days,
        'features': plan.features
    } for plan in plans])

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subscription(request):
    """Create a new subscription"""
    try:
        plan_id = request.data.get('plan_id')
        plan = SubscriptionPlan.objects.get(id=plan_id)
        
        # Create or get Stripe customer
        if not request.user.stripe_customer_id:
            customer = stripe.Customer.create(
                email=request.user.email,
                metadata={'user_id': request.user.id}
            )
            request.user.stripe_customer_id = customer.id
            request.user.save()
        
        # Create Stripe subscription
        subscription = stripe.Subscription.create(
            customer=request.user.stripe_customer_id,
            items=[{'price': plan.stripe_price_id}],
            payment_behavior='default_incomplete',
            payment_settings={'save_default_payment_method': 'on_subscription'},
            expand=['latest_invoice.payment_intent'],
        )
        
        # Create subscription record
        user_subscription = UserSubscription.objects.create(
            user=request.user,
            plan=plan,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=plan.duration_days),
            stripe_subscription_id=subscription.id,
            stripe_customer_id=request.user.stripe_customer_id
        )
        
        return Response({
            'subscription_id': subscription.id,
            'client_secret': subscription.latest_invoice.payment_intent.client_secret
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_subscription(request):
    """Cancel current subscription"""
    try:
        subscription = UserSubscription.objects.get(
            user=request.user,
            status='active'
        )
        
        # Cancel Stripe subscription
        stripe.Subscription.delete(subscription.stripe_subscription_id)
        
        # Update subscription status
        subscription.status = 'canceled'
        subscription.save()
        
        return Response({'message': 'Subscription cancelled successfully'})
        
    except UserSubscription.DoesNotExist:
        return Response({'error': 'No active subscription found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subscription_status(request):
    """Get current subscription status"""
    try:
        subscription = UserSubscription.objects.get(
            user=request.user,
            status='active'
        )
        
        return Response({
            'plan_name': subscription.plan.name,
            'start_date': subscription.start_date,
            'end_date': subscription.end_date,
            'features': subscription.plan.features,
            'is_active': subscription.is_active()
        })
        
    except UserSubscription.DoesNotExist:
        return Response({'error': 'No active subscription found'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payment_history(request):
    """Get user's payment history"""
    payments = PaymentHistory.objects.filter(user=request.user).order_by('-payment_date')
    return Response([{
        'amount': payment.amount,
        'status': payment.status,
        'payment_date': payment.payment_date,
        'plan_name': payment.subscription.plan.name
    } for payment in payments])