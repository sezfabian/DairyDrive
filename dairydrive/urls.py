from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('farms/', include('farms.urls')),
    path('animals/', include('animals.urls')),
]