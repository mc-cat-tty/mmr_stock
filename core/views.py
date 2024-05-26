from django.shortcuts import render
from rest_framework import serializers, viewsets
from django.http import HttpResponse
from .models import Component

class ComponentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Component
    fields = ('id', 'name', 'code', 'picture', 'datasheet_url', 'quantity', 'row', 'column', 'depth', 'protection')

class ComponentViewSet(viewsets.ModelViewSet):
  queryset = Component.objects.all()
  serializer_class = ComponentSerializer
