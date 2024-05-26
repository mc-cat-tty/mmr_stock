from django.shortcuts import render
from core.models import Component
from rest_framework import serializers, generics
from django.http import HttpResponse

class ComponentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Component
    fields = ('id', 'name', 'code', 'picture', 'datasheet_url', 'quantity', 'row', 'column', 'depth', 'protection')

class ComponentListAPIView(generics.ListAPIView):
  queryset = Component.objects.all()
  serializer_class = ComponentSerializer

