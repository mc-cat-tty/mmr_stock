from django.urls import path
from rest_framework import routers
from .views import ComponentViewSet
from django.urls import path
from django.shortcuts import render

router = routers.SimpleRouter()
router.register(r'components', ComponentViewSet, r'components')

app_name = "core"

urlpatterns = [
  path("home/", lambda request: render(request, template_name="home.html"), name='home')
] + router.urls