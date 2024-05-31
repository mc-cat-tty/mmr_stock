from rest_framework import serializers, status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import *

class RequestSerializer(serializers.ModelSerializer):
  component_name = serializers.CharField(source="component.name")
  component_code = serializers.CharField(source="component.code")
  profile_name = serializers.CharField(source="profile.user.username")
  
  class Meta:
    model = Request
    fields = ('id', 'approved', 'quantity', 'date', 'profile_name', 'component_name', 'component_code')

class UpdateRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = Request
    fields = ('id', 'approved')

class RequestAPI(GenericViewSet, UpdateModelMixin):
  queryset = Request.objects.all()
  serializer_class = UpdateRequestSerializer

  def update(self, request: Request, *args, **kwargs) -> Response:
    pk = kwargs.get('pk')
    request_obj = self.queryset.get(pk=pk)
    if request_obj.approved != None: return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    user_pk = request_obj.profile.pk
    group_name = f"user_{user_pk}"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
      group_name,
      {
        "type": "request_update",
        "request_pk": pk,
      }
    )
    return super().update(request, *args, **kwargs)