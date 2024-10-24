from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('farms/', include('farms.urls')),
    path('animals/', include('animals.urls')),
    path('feeds/', include('feeds.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)