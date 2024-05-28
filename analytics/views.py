from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from rest_framework import generics, serializers
from .models import Star

def favorites(request: HttpRequest) -> HttpResponse:
  context = {
    'pagename': 'Favorites',
  }

  return render(request, template_name="favorites.html", context=context)

class StarSerializer(serializers.Serializer):
  class Meta:
    model = Star
    fields = ("user", "component")

class StarCreateAPIView(generics.CreateAPIView):
  queryset = Star.objects.all()
  serializer_class = StarSerializer
