from django.urls import path
from django.urls import path
from rest_framework import routers

from .home_views import HomeView, FavoritesView
from .component_views import ComponentAPI
from .request_views import RequestAPI
from .views import LoginView, LogoutView

STATIC_URL = "/media/static"
app_name = "core"

router = routers.SimpleRouter()
router.register(r'components', ComponentAPI, r'components')
router.register(r'requests', RequestAPI, r'requests')

urlpatterns = [
  path("", HomeView.as_view(), name='home'),
  path("login/", LoginView.as_view(), name="login"),
  path("logout/", LogoutView.as_view(), name="logout"),
  path("favorites/", FavoritesView.as_view(), name='favorites'),
] + router.urls