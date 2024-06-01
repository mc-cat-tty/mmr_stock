from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import serializers
from .models import *
from .request_views import NotifyRequestsMixin 

class ComponentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Component
    fields = ('__all__')

class ComponentPermissions(BasePermission):
  def has_permission(self, request: Request, view: APIView):
    if not isinstance(view, ComponentAPI): return False

    if request.method in SAFE_METHODS or request.user.is_staff:
      return True
    
    if request.user.is_authenticated and request.method == "PATCH":
      return True

    return False

class ComponentAPI(
  GenericViewSet,
  RetrieveModelMixin,
  UpdateModelMixin,
  CreateModelMixin,
  DestroyModelMixin,
  NotifyRequestsMixin):
  queryset = Component.objects.all()
  serializer_class = ComponentSerializer
  permission_classes = [ComponentPermissions]

  def partial_update(self, request: Request, *args, **kwargs) -> Response:
    pk = kwargs.get('pk')
    component = get_object_or_404(Component, pk=pk)
    available_quantity = component.quantity
    
    try:
      requested_quantity = int(request.data.get('quantity'))
    except:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    
    available_quantity -= requested_quantity
    
    if (available_quantity < 0):
      return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

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