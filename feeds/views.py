from django.contrib.auth.models import User
from users.models import UserProfile
from farms.models import Farm
from animals.models import AnimalType
from users.functions import fix_phone_number
from .serializers import *
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
from datetime import datetime
import random
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_feeds_records(request, farm_id):
    """Get feeds"""
    farm = Farm.objects.get(id=farm_id)
    # get feed types
    feedTypes = AnimalFeedType.objects.filter(farm=farm)
    typeserializer = AnimalFeedTypeSerializer(feedTypes, many=True)

    # get feeds
    feeds = AnimalFeed.objects.filter(animal_feed_type__in=feedTypes)
    feedserializer = AnimalFeedSerializer(feeds, many=True)

    # get feed entries
    feedEntrys = AnimalFeedEntry.objects.filter(animal_feed__in=feeds).order_by('-created_at')
    entryserializer = AnimalFeedEntrySerializer(feedEntrys, many=True)

    # get feed purchases
    feedPurchases = AnimalFeedPurchase.objects.filter(animal_feed__in=feeds)
    purchaseserializer = AnimalFeedPurchaseSerializer(feedPurchases, many=True)

    return Response({"feedTypes": typeserializer.data, "feeds": feedserializer.data, "feedEntries": entryserializer.data, "feedPurchases": purchaseserializer.data}, status=200)


# Feed Type Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_feed_types(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    feed_types = AnimalFeedType.objects.filter(farm=farm)
    serializer = AnimalFeedTypeSerializer(feed_types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_feed_type(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    feed_type = get_object_or_404(AnimalFeedType, id=id, farm=farm)
    serializer = AnimalFeedTypeSerializer(feed_type)
    return Response(serializer.data)

@api_view(['POST'])
def add_feed_type(request, farm_id):
    """Add feed type"""
    request.data["farm"] = farm_id
    request.data["created_by"] = request.user.id
    serializer = AnimalFeedTypeSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data["name"] in [type.name for type in AnimalFeedType.objects.filter(farm=farm_id)]:
            return Response({"error": "Feed type with this name already exists"}, status=400)
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def edit_feed_type(request, farm_id, id):
    """Edit feed type"""
    # check if feed type exists
    request.data["farm"] = farm_id
    farm = get_object_or_404(Farm, id=farm_id)
    try:
        feed_type = AnimalFeedType.objects.get(id=id, farm=farm)
        serializer = AnimalFeedTypeSerializer(feed_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
        
    except AnimalFeedType.DoesNotExist:
        return Response({"error": f"Feed type with this id:{id} does not exist"}, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_feed_type(request, farm_id, id):
    """Delete feed type"""
    # check if feed type exists
    farm = get_object_or_404(Farm, id=farm_id)
    try:
        feed_type = AnimalFeedType.objects.get(id=id, farm=farm)
        # check if feed type is used by any feed
        feeds = AnimalFeed.objects.filter(animal_feed_type=feed_type)
        if len(feeds) > 0:
            return Response({"error": f"Feed type with this id:{id} is used by recorded animal feeds"}, status=400)
        feed_type.delete()
        return Response({"message": "Feed type deleted successfully"}, status=200)
    except AnimalFeedType.DoesNotExist:
        return Response({"error": f"Feed type with this id:{id} does not exist on your farm"}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_feeds(request, farm_id):
    """Get all feeds"""
    try:
        feeds = AnimalFeed.objects.filter(farm=farm_id)
        serializer = AnimalFeedSerializer(feeds, many=True)
        return Response(serializer.data, status=200)
    except AnimalFeed.DoesNotExist:
        return Response({"error": "No feeds found"}, status=404)


@api_view(['POST'])
def add_feed(request, farm_id):
    """Add feed"""
    request.data["farm"] = farm_id
    request.data["created_by"] = request.user.id
    serializer = AnimalFeedSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_feed(request, farm_id, id):
    """Edit feed"""
    farm = get_object_or_404(Farm, id=farm_id)
    feed = AnimalFeed.objects.get(id=id, farm=farm)
    request.data["farm"] = farm_id
    serializer = AnimalFeedSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        feed = AnimalFeed.objects.get(id=id)
        for key, value in request.data.items():
            if key != "id" and key != "created_by" and key != "farm":
                if key == "animal_feed_type":
                    feed_type = AnimalFeedType.objects.get(id=value)
                    setattr(feed, key, feed_type)
                elif key == "animal_types":
                    for animal_type in value:
                        animal_type = AnimalType.objects.get(id=animal_type)
                        feed.animal_types.add(animal_type)
                else:
                    setattr(feed, key, value)
        feed.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_feed(request, farm_id, id):
    """Delete feed"""
    # # Check if userprofile has admin role
    # if UserProfile.objects.get(user=request.user).role != "Admin":
    #     return Response({"error": "Only Admins can delete farm records"}, status=400)
    # check if feed exists
    try:
        farm = get_object_or_404(Farm, id=farm_id)
        feed = AnimalFeed.objects.get(id=id, farm=farm)
        # check if feed is used by any feed entry or feed purchase
        feed_entries = AnimalFeedEntry.objects.filter(animal_feed=feed)
        if len(feed_entries) > 0:
            return Response({"error": f"Feed with this id:{id} is used by recorded feed entries"}, status=400)
        
        feed_purchases = AnimalFeedPurchase.objects.filter(animal_feed=feed)
        if len(feed_purchases) > 0:
            return Response({"error": f"Feed with this id:{id} is used by recorded feed purchases"}, status=400)
        
        feed.delete()
        return Response({"message": "Feed deleted successfully"}, status=200)
    except AnimalFeed.DoesNotExist:
        return Response({"error": f"Feed with this id:{id} does not exist"}, status=400)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_feed_entry(request, farm_id):
    """Add feed entry"""
    request.data["farm"] = farm_id
    request.data["created_by"] = request.user.id
    serializer = AnimalFeedEntrySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_feed_entry(request, id):
    """Delete feed entry"""
    #Check if user role is admin
    if UserProfile.objects.get(user=request.user).role != "Admin" and UserProfile.objects.get(user=request.user).role != "Manager":
        return Response({"error": "You do not have permission to delete this feed"}, status=400)

    # check if feed entry exists
    try:
        feed_entry = AnimalFeedEntry.objects.get(id=id)
        if feed_entry.is_deleted:
            return Response({"error": f"Feed entry with this id:{id} is already deleted"}, status=400)
        feed_entry.is_deleted = True
        feed_entry.deleted_by = request.user
        feed_entry.deleted_at = datetime.now()
        feed_entry.save()

        serializer = AnimalFeedEntrySerializer(feed_entry)
        return Response({"message": "Feed entry deleted successfully", "feed_entry": serializer.data}, status=200)
    except AnimalFeedEntry.DoesNotExist:
        return Response({"error": f"Feed entry with this id:{id} does not exist"}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_feed_purchase(request, farm_id):
    """Add feed purchase"""
    farm = Farm.objects.get(id=farm_id)
    request.data["created_by"] = request.user.id
    serializer = AnimalFeedPurchaseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_feed_purchase(request, id):
    """Delete feed purchase"""
    #Check if user role is admin
    if UserProfile.objects.get(user=request.user).role != "Admin" and UserProfile.objects.get(user=request.user).role != "Manager":
        return Response({"error": "You do not have permission to delete this feed"}, status=400)

    # check if feed purchase exists
    try:
        feed_purchase = AnimalFeedPurchase.objects.get(id=id)
        if feed_purchase.is_deleted:
            return Response({"error": f"Feed purchase with this id:{id} is already deleted"}, status=400)
        feed_purchase.is_deleted = True
        feed_purchase.deleted_by = request.user
        feed_purchase.deleted_at = datetime.now()
        feed_purchase.save()
        serializer = AnimalFeedPurchaseSerializer(feed_purchase)
        return Response({"message": "Feed purchase deleted successfully", "feed_purchase": serializer.data}, status=200)
    except AnimalFeedPurchase.DoesNotExist:
        return Response({"error": f"Feed purchase with this id:{id} does not exist"}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_feed(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    feed = get_object_or_404(AnimalFeed, id=id, farm=farm)
    serializer = AnimalFeedSerializer(feed)
    return Response(serializer.data)



# Feed Entry Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_feed_entries(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    feed_id = request.query_params.get('feed_id')
    animal_id = request.query_params.get('animal_id')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    entries = AnimalFeedEntry.objects.filter(farm=farm)
    
    if feed_id:
        entries = entries.filter(animal_feed_id=feed_id)
    if animal_id:
        entries = entries.filter(animal_id=animal_id)
    if start_date:
        entries = entries.filter(created_at__gte=start_date)
    if end_date:
        entries = entries.filter(created_at__lte=end_date)

    serializer = AnimalFeedEntrySerializer(entries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_feed_entry(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    entry = get_object_or_404(AnimalFeedEntry, id=id, farm=farm)
    serializer = AnimalFeedEntrySerializer(entry)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_feed_entry(request, farm_id, id):
    request.data["farm"] = farm_id
    request.data["created_by"] = request.user.id
    farm = get_object_or_404(Farm, id=farm_id)
    entry = get_object_or_404(AnimalFeedEntry, id=id, farm=farm)
    serializer = AnimalFeedEntrySerializer(entry, data=request.data)
    if serializer.is_valid():
        serializer.save(farm=farm)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_feed_entry(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    entry = get_object_or_404(AnimalFeedEntry, id=id, farm=farm)
    entry.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Feed Purchase Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_feed_purchases(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, )
    feed_id = request.query_params.get('feed_id')
    supplier_id = request.query_params.get('supplier_id')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    payment_status = request.query_params.get('payment_status')

    purchases = AnimalFeedPurchase.objects.filter(farm=farm)
    
    if feed_id:
        purchases = purchases.filter(animal_feed_id=feed_id)
    if supplier_id:
        purchases = purchases.filter(supplier_id=supplier_id)
    if start_date:
        purchases = purchases.filter(created_at__gte=start_date)
    if end_date:
        purchases = purchases.filter(created_at__lte=end_date)
    if payment_status is not None:
        purchases = purchases.filter(payment_status=payment_status.lower() == 'true')

    serializer = AnimalFeedPurchaseSerializer(purchases, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_feed_purchase(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    purchase = get_object_or_404(AnimalFeedPurchase, id=id, farm=farm)
    serializer = AnimalFeedPurchaseSerializer(purchase)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_feed_purchase(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    serializer = AnimalFeedPurchaseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(farm=farm)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_feed_purchase(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    purchase = get_object_or_404(AnimalFeedPurchase, id=id, farm=farm)
    serializer = AnimalFeedPurchaseSerializer(purchase, data=request.data)
    if serializer.is_valid():
        serializer.save(farm=farm)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_feed_purchase(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    purchase = get_object_or_404(AnimalFeedPurchase, id=id, farm=farm)
    purchase.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_feed_purchase_as_paid(request, farm_id, id):
    farm = get_object_or_404(Farm, id=farm_id)
    purchase = get_object_or_404(AnimalFeedPurchase, id=id, farm=farm)
    purchase.payment_status = True
    purchase.save()
    return Response({'status': 'payment marked as completed'})