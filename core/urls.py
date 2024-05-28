from django.urls import path
from rest_framework import routers
from .views import ComponentViewSet, home
from django.urls import path

STATIC_URL = "/media/static"

router = routers.SimpleRouter()
router.register(r'components', ComponentViewSet, r'components')

app_name = "core"

urlpatterns = [
  path("", home, name='home')
] + router.urls