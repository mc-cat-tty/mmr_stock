from typing import Text
from django.shortcuts import render
from rest_framework import serializers, viewsets
from django.http import HttpResponse, HttpRequest
from .models import Component
from django.shortcuts import render
from django.db.models import CharField, TextField, IntegerField
from operator import attrgetter

def home(request: HttpRequest) -> HttpResponse:
  component_text_fields = filter(
    lambda field: isinstance(field, CharField) or isinstance(field, TextField),
    Component._meta.fields
  )

  component_numeric_fields = filter(
    lambda field: isinstance(field, IntegerField) and field.name != 'id',
    Component._meta.fields
  )

  context = {
    'pagename': 'Home',
    'recommended': Component.objects.all()[:20],
    'components': Component.objects.all()[:12],
    'modal_textual_fields': component_text_fields,
    'modal_numeric_fields': component_numeric_fields
  }

  return render(request, template_name="home.html", context=context)

def favorites(request: HttpRequest) -> HttpResponse:
  context = {
    'pagename': 'Favorites',
    'starred': Component.objects.all()
  }

  return render(request, template_name="starred.html", context=context)

class ComponentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Component
    fields = ('id', 'name', 'code', 'picture', 'datasheet_url', 'quantity', 'row', 'column', 'depth', 'protection')

class ComponentViewSet(viewsets.ModelViewSet):
  queryset = Component.objects.all()
  serializer_class = ComponentSerializer