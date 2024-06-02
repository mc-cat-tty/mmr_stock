from django.urls import path
from channels.routing import URLRouter
from .admin_views import DashView, DashDetailView, DashUpdatesAPI
from .user_views import MailboxView

STATIC_URL = "/media/static"
app_name = "dash"

urlpatterns = [
  path(r'', DashView.as_view(), name=r''),
  path(r'mailbox', MailboxView.as_view(), name=r'mailbox'),
  path(r'user/<int:id>', DashDetailView.as_view())
]

ws_urlpatterns = [
  path('dash/updates/<int:user_id>', DashUpdatesAPI.as_asgi())
]