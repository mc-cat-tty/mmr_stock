from django.urls import path
from .views import StarAPI
from rest_framework import routers

STATIC_URL = "/media/static"
app_name = "analytics"


router = routers.SimpleRouter()
router.register(r'favorites', StarAPI, "favorites")
urlpatterns = router.urls