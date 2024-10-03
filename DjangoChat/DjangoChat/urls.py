# DjangoChat/urls.py

from django.contrib import admin
from django.urls import path, include  # Ensure include is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("ChitChat.urls")),  # Ensure ChitChat.urls is included
]
