from typing import Text
from django.shortcuts import render
from rest_framework import serializers, viewsets
from django.http import HttpResponse, HttpRequest
from .models import Component
from django.shortcuts import render
from django.db.models import CharField, TextField
from operator import attrgetter

def home(request: HttpRequest) -> HttpResponse:
  component_text_fields = tuple(
    filter(
      lambda field: isinstance(field, CharField) or isinstance(field, TextField),
      Component._meta.fields
    )
  )
  context = {
    'recommended': Component.objects.all()[:20],
    'components': Component.objects.all()[:9],
    'modal_textual_fields': map(
      attrgetter('name'),
      component_text_fields
    )
  }
  return render(request, template_name="home.html", context=context)

class ComponentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Component
    fields = ('id', 'name', 'code', 'picture', 'datasheet_url', 'quantity', 'row', 'column', 'depth', 'protection')

class ComponentViewSet(viewsets.ModelViewSet):
  queryset = Component.objects.all()
  serializer_class = ComponentSerializer