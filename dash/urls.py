from django.urls import path
from .views import DashView

STATIC_URL = "/media/static"
app_name = "dash"

urlpatterns = [
  path(r'', DashView.as_view(), name=r'')
]