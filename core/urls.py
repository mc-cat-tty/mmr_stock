from django.urls import path
from rest_framework import routers
from django.urls import path

from .home_views import HomeView, FavoritesView
from .component_views import ComponentAPI
from .request_views import RequestAPI

STATIC_URL = "/media/static"
app_name = "core"

router = routers.SimpleRouter()
router.register(r'components', ComponentAPI, r'components')
router.register(r'requests', RequestAPI, r'requests')

urlpatterns = [
  path("", HomeView.as_view(), name='home'),
  path("favorites", FavoritesView.as_view(), name='favorites'),
] + router.urls