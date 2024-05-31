from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import *
from .request_views import NotifyRequestsMixin 


class ComponentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Component
    fields = (
      'id', 'name', 'code',
      'picture', 'datasheet_url',
      'quantity', 'row', 'column',
      'depth', 'protection'
    )

class ComponentAPI(
  GenericViewSet,
  RetrieveModelMixin,
  UpdateModelMixin,
  CreateModelMixin,
  DestroyModelMixin,
  NotifyRequestsMixin):
  queryset = Component.objects.all()
  serializer_class = ComponentSerializer

  def partial_update(self, request: Request, *args, **kwargs) -> Response:
    pk = kwargs.get('pk')
    component = Component.objects.get(pk=pk)
    available_quantity = component.quantity
    requested_quantity = int(request.data.get('quantity'))
    available_quantity -= requested_quantity
    
    if (available_quantity < 0): return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    Component.objects.filter(pk=pk).update(quantity = available_quantity)
    if not component.protection:
      Use.objects.create(
        profile=Profile.objects.get(user=self.request.user),
        component=component,
        date=timezone.now(),
        quantity=requested_quantity
      )
      action = 'get'
    else:
      r = Request.objects.create(
        profile=Profile.objects.get(user=self.request.user),
        component=component,
        date=timezone.now(),
        quantity=requested_quantity
      )
      self.notify_add(self.request.user.pk, r.pk)
      action = 'request'

    state = {
      'quantity': requested_quantity,
      'action': action
    }
    return Response(status=status.HTTP_200_OK, data=state)