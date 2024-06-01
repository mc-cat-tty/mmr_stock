from django.urls import path
from rest_framework import routers
from .views import StarAPI

STATIC_URL = "/media/static"
app_name = "analytics"

router = routers.SimpleRouter()
router.register(r'favorites', StarAPI, "favorites")
urlpatterns = router.urls