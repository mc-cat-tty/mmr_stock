from django.shortcuts import render
from rest_framework import serializers, viewsets
from django.http import HttpResponse, HttpRequest
from .models import Component
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
  context = {
    'recommended': Component.objects.all()[:20],
    'components': Component.objects.all()
  }
  return render(request, template_name="home.html", context=context)

class ComponentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Component
    fields = ('id', 'name', 'code', 'picture', 'datasheet_url', 'quantity', 'row', 'column', 'depth', 'protection')

class ComponentViewSet(viewsets.ModelViewSet):
  queryset = Component.objects.all()
  serializer_class = ComponentSerializer