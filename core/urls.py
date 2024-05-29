from django.urls import path
from rest_framework import routers
from .views import ComponentAPI, HomeView, FavoritesView
from django.urls import path

STATIC_URL = "/media/static"
app_name = "core"

router = routers.SimpleRouter()
router.register(r'components', ComponentAPI, r'components')

urlpatterns = [
  path("", HomeView.as_view(), name='home'),
  path("favorites", FavoritesView.as_view(), name='favorites'),
] + router.urls