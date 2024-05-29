from django.urls import path
from django.urls import path
from .views import StarAPIView
from rest_framework import routers

STATIC_URL = "/media/static"
app_name = "analytics"


router = routers.SimpleRouter()
router.register(r'favorites', StarAPIView, "favorites")
urlpatterns = router.urls