from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.request import Request
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

class StarAPIView(viewsets.ViewSet):
  def create(self, request, pk=None):
    pass
  
  def list(self, request: Request):
    queryset = Star.objects.all()
    serializer = StarSerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    pass

  def destroy(self, request, pk=None):
    pass
