from django.urls import path
from channels.routing import URLRouter
from .views import DashView, DashDetailView, DashUpdatesAPI

STATIC_URL = "/media/static"
app_name = "dash"

urlpatterns = [
  path(r'', DashView.as_view(), name=r''),
  path(r'user/<int:id>', DashDetailView.as_view())
]

ws_urlpatterns = [
  path('dash/updates', DashUpdatesAPI.as_asgi())
]