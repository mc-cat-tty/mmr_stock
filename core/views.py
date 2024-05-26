from django.shortcuts import render
from core.models import Component
from rest_framework import serializers, generics
from django.http import HttpResponse

class ComponentSerializer(serializers.Serializer):
  class Meta:
    model = Component
    fields = ('id', 'name')

class ComponentListAPIView(generics.ListAPIView):
  queryset = Component.objects.all()[:10]
  serializer_class = ComponentSerializer

