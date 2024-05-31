from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.template.defaultfilters import date, time


from .models import *

class RequestSerializer(serializers.ModelSerializer):
  component_name = serializers.CharField(source="component.name")
  component_code = serializers.CharField(source="component.code")
  component_pic = serializers.ImageField(source="component.picture")
  profile_name = serializers.CharField(source="profile.user.username")
  
  class Meta:
    model = Request
    fields = (
      'id', 'approved', 'quantity',
      'date', 'profile_name', 'component_name',
      'component_code', 'component_pic'
    )
  
  def to_representation(self, instance):
    r = super().to_representation(instance)
    r['date'] = date(instance.date, "SHORT_DATE_FORMAT") + " " + time(instance.date, "G:i")
    return r

class UpdateRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = Request
    fields = ('id', 'approved')

class NotifyRequestsMixin:
  def notify(self, user_pk: int, request_pk: int) -> None:
    group_name = f"user_{user_pk}"
    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)(
      group_name,
      {
        "type": "request_add",
        "request_pk": request_pk,
      }
    )

    async_to_sync(channel_layer.group_send)(
      "user_all",
      {
        "type": "request_add",
        "request_pk": request_pk,
      }
    )

class RequestAPI(GenericViewSet, UpdateModelMixin, NotifyRequestsMixin):
  queryset = Request.objects.all()
  serializer_class = UpdateRequestSerializer

  def update(self, request: Request, *args, **kwargs) -> Response:
    pk = kwargs.get('pk')
    request_obj = self.queryset.get(pk=pk)
    if request_obj.approved != None: return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    if request.data.get('approved') == 'true':
      Use.objects.create(
        profile = request_obj.profile,
        component = request_obj.component,
        date = timezone.now(),
        quantity = request_obj.quantity
      )
    
    return super().update(request, *args, **kwargs)