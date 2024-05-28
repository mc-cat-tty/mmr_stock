from django.urls import path
from rest_framework import routers
from .views import ComponentViewSet, home
from django.urls import path

STATIC_URL = "/media/static"
app_name = "core"

router = routers.SimpleRouter()
router.register(r'components', ComponentViewSet, r'components')

urlpatterns = [
  path("", home, name='home')
] + router.urls