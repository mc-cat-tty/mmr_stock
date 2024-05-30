from rest_framework import serializers, status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response

from .models import *

class RequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = Request
    fields = ('id', 'approved')

class RequestAPI(GenericViewSet, UpdateModelMixin):
  queryset = Request.objects.all()
  serializer_class = RequestSerializer

  def update(self, request: Request, *args, **kwargs) -> Response:
    pk = kwargs.get('pk')
    request_obj = self.queryset.get(pk=pk)
    if request_obj.approved != None: return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    return super().update(request, *args, **kwargs)