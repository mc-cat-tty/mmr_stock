from django.urls import path
from .views import favorites
from django.urls import path

STATIC_URL = "/media/static"
app_name = "analytics"

urlpatterns = [
  path("favorites/", favorites, name='favorites')
]