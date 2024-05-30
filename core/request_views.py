from rest_framework import serializers
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import *

class RequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = Request
    fields = ('id', 'approved')

class RequestAPI(GenericViewSet, UpdateModelMixin):
  queryset = Request.objects.all()
  serializer_class = RequestSerializer