from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Feed Type URLs
    path('get_feed_types/<int:farm_id>', views.get_feed_types, name='get_feed_types'),
    path('get_feed_type/<int:farm_id>/<int:id>', views.get_feed_type, name='get_feed_type'),
    path('add_feed_type/<int:farm_id>', views.add_feed_type, name='add_feed_type'),
    path('edit_feed_type/<int:farm_id>/<int:id>', views.edit_feed_type, name='edit_feed_type'),
    path('delete_feed_type/<int:farm_id>/<int:id>', views.delete_feed_type, name='delete_feed_type'),

    # Feed URLs
    path('get_feeds/<int:farm_id>', views.get_feeds, name='get_feeds'),
    path('get_feed/<int:farm_id>/<int:id>', views.get_feed, name='get_feed'),
    path('add_feed/<int:farm_id>', views.add_feed, name='add_feed'),
    path('edit_feed/<int:farm_id>/<int:id>', views.edit_feed, name='edit_feed'),
    path('delete_feed/<int:farm_id>/<int:id>', views.delete_feed, name='delete_feed'),

    # Feed Entry URLs
    path('get_feed_entries/<int:farm_id>', views.get_feed_entries, name='get_feed_entries'),
    path('get_feed_entry/<int:farm_id>/<int:id>', views.get_feed_entry, name='get_feed_entry'),
    path('add_feed_entry/<int:farm_id>', views.add_feed_entry, name='add_feed_entry'),
    path('edit_feed_entry/<int:farm_id>/<int:id>', views.edit_feed_entry, name='edit_feed_entry'),
    path('delete_feed_entry/<int:farm_id>/<int:id>', views.delete_feed_entry, name='delete_feed_entry'),

    # Feed Purchase URLs
    path('get_feed_purchases/<int:farm_id>', views.get_feed_purchases, name='get_feed_purchases'),
    path('get_feed_purchase/<int:farm_id>/<int:id>', views.get_feed_purchase, name='get_feed_purchase'),
    path('add_feed_purchase/<int:farm_id>', views.add_feed_purchase, name='add_feed_purchase'),
    path('edit_feed_purchase/<int:farm_id>/<int:id>', views.edit_feed_purchase, name='edit_feed_purchase'),
    path('delete_feed_purchase/<int:farm_id>/<int:id>', views.delete_feed_purchase, name='delete_feed_purchase'),
    path('mark_feed_purchase_as_paid/<int:farm_id>/<int:id>', views.mark_feed_purchase_as_paid, name='mark_feed_purchase_as_paid'),
]