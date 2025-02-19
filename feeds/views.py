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

@api_view(['GET'])
def get_feeds(request, farm_id):
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

@api_view(['POST'])
def edit_feed_type(request, id):
    """Edit feed type"""
    # check if feed type exists
    try:
        feed_type = AnimalFeedType.objects.get(id=id)

        serializer = AnimalFeedTypeSerializer(feed_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
        
    except AnimalFeedType.DoesNotExist:
        return Response({"error": f"Feed type with this id:{id} does not exist"}, status=400)

@api_view(['DELETE'])
def delete_feed_type(request, id):
    """Delete feed type"""
    # check if feed type exists
    try:
        feed_type = AnimalFeedType.objects.get(id=id)
        # check if feed type is used by any feed
        feeds = AnimalFeed.objects.filter(animal_feed_type=feed_type)
        if len(feeds) > 0:
            return Response({"error": f"Feed type with this id:{id} is used by recorded animal feeds"}, status=400)
        feed_type.delete()
        return Response({"message": "Feed type deleted successfully"}, status=200)
    except AnimalFeedType.DoesNotExist:
        return Response({"error": f"Feed type with this id:{id} does not exist"}, status=400)


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


@api_view(['POST'])
def edit_feed(request, id):
    """Edit feed"""
    feed = AnimalFeed.objects.get(id=id)
    request.data["farm"] = feed.farm.id
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

@api_view(['POST'])
def delete_feed(request, id):
    """Delete feed"""
    # Check if userprofile has admin role
    if UserProfile.objects.get(user=request.user).role != "Admin":
        return Response({"error": "You do not have permission to delete this feed"}, status=400)
    # check if feed exists
    try:
        feed = AnimalFeed.objects.get(id=id)
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