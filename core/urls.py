from django.urls import path
from rest_framework import routers
from .views import ComponentViewSet

router = routers.SimpleRouter()
router.register(r'components', ComponentViewSet, r'components')

urlpatterns = router.urls