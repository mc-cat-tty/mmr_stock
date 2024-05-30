from django.urls import path
from .views import DashView, DashDetailView

STATIC_URL = "/media/static"
app_name = "dash"

urlpatterns = [
  path(r'', DashView.as_view(), name=r''),
  path(r'user/<int:id>', DashDetailView.as_view())
]