from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import date, time
from django.utils.formats import time_format
from rest_framework import serializers, status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import *

class RequestSerializer(serializers.ModelSerializer):
  """
  Serialize all instrinsics and related fields of a request. Used
  over websockets by real-time dashboard.
  """
  component_name = serializers.CharField(source="component.name")
  component_code = serializers.CharField(source="component.code")
  component_pic = serializers.ImageField(source="component.picture")
  profile_name = serializers.CharField(source="profile.user.username")
  
  class Meta:
    model = Request
    fields = "__all__"
  
  def to_representation(self, instance):
    r = super().to_representation(instance)
    r['date'] = date(instance.date, "SHORT_DATE_FORMAT") + " " + time_format(instance.date, "G:i")
    return r

class UpdateRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = Request
    fields = ('id', 'approved')

class NotifyRequestsMixin:
  def __notify(self, user_pk: int, request_pk: int, type: str) -> None:
    group_name = f"user_{user_pk}"
    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)(
      group_name,
      {
        "type": type,
        "request_pk": request_pk,
      }
    )

    async_to_sync(channel_layer.group_send)(
      "user_all",
      {
        "type": type,
        "request_pk": request_pk,
      }
    )
  
  def notify_add(self, user_pk: int, request_pk: int) -> None:
    return self.__notify(user_pk, request_pk, "request_add")
  
  def notify_approval(self, user_pk: int, request_pk: int) -> None:
    return self.__notify(user_pk, request_pk, "request_approve")
  
  def notify_rejection(self, user_pk: int, request_pk: int) -> None:
    return self.__notify(user_pk, request_pk, "request_reject")


class RequestAPI(GenericViewSet, UpdateModelMixin, NotifyRequestsMixin):
  queryset = Request.objects.all()
  serializer_class = UpdateRequestSerializer
  permission_classes = [IsAdminUser]

  def update(self, request: Request, *args, **kwargs) -> Response:
    pk = kwargs.get('pk')
    request_obj = get_object_or_404(self.queryset, pk=pk)
    if request_obj.is_processed():
      return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    if request.data.get('approved') == 'true':
      Use.objects.create(
        profile = request_obj.profile,
        component = request_obj.component,
        date = timezone.now(),
        quantity = request_obj.quantity
      )
      self.notify_approval(request_obj.profile.user.pk, request_obj.pk)
    else:
      self.notify_rejection(request_obj.profile.user.pk, request_obj.pk)
    
    return super().update(request, *args, **kwargs)