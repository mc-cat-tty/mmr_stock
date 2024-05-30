from django.urls import path
from .views import test

STATIC_URL = "/media/static"
app_name = "dash"

urlpatterns = [
  path(r'', test, name=r'')
]