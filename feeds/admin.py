from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

admin.site.register(AnimalFeed)
admin.site.register(AnimalFeedType)
admin.site.register(AnimalFeedEntry)
admin.site.register(AnimalFeedPurchase)
