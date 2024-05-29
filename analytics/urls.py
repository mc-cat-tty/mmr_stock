from django.urls import path
from django.urls import path
from .views import StarAPIView

STATIC_URL = "/media/static"
app_name = "analytics"

# urlpatterns = [
#   path("favorites/", favorites, name="favorites"),
#   path("favorites/add/", StarCreateAPIView.as_view()),
# ]

from .views import Star
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'favorites', StarAPIView, "favorites")
urlpatterns = router.urls