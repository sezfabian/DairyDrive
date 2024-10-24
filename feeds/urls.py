from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Get Feeds
    path("get_feeds/<int:farm_id>", get_feeds, name="get_feeds"),

    # Feed Types
    path("add_feed_type/<int:farm_id>", add_feed_type, name="add_feed_type"),
    path("edit_feed_type/<int:id>", edit_feed_type, name="edit_feed_type"),
    path("delete_feed_type/<int:id>", delete_feed_type, name="delete_feed_type"),

    # Feeds
    path("create_feed/<int:farm_id>", add_feed, name="create_feed"),
    path("edit_feed/<int:id>", edit_feed, name="edit_feed"),
    path("delete_feed/<int:id>", delete_feed, name="delete_feed"),

    # Feed Entries
    path("create_feed_entry/<int:farm_id>", add_feed_entry, name="create_feed_entry"),
    path("delete_feed_entry/<int:id>", delete_feed_entry, name="delete_feed_entry"),

    # Feed Purchases
    path("create_feed_purchase/<int:farm_id>", add_feed_purchase, name="create_feed_purchase"),
    path("delete_feed_purchase/<int:id>", delete_feed_purchase, name="delete_feed_purchase"),

]