from django.urls import path
from core.views import ComponentListAPIView

urlpatterns = [
  path('components/', ComponentListAPIView.as_view())
]