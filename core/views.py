from statistics import quantiles
from django.db.models import CharField, TextField, IntegerField
from django.views.generic.list import ListView
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import *


class HomeView(ListView):
  model = Component
  template_name="home.html"
  paginate_by = 24
  form_data = {}
  
  def get_queryset(self):
    queryset = super().get_queryset()

    query = self.request.GET.get('query', '')
    queryset = queryset.filter(code__icontains=query) | queryset.filter(name__icontains=query)
    min_quantity = self.request.GET.get('min', '')
    max_quantity = self.request.GET.get('max', '')
    
    try:
      queryset = queryset.filter(quantity__gte=int(min_quantity))
    except:
      pass
    
    try:
      queryset = queryset.filter(quantity__lte=int(max_quantity))
    except:
      pass

    self.form_data = {
      'min_quantity': min_quantity,
      'max_quantity': max_quantity,
      'query': query
    }

    return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    COMPONENT_TEXT_FIELDS = filter(
      lambda field: isinstance(field, CharField) or isinstance(field, TextField),
      Component._meta.fields
    )
    COMPONENT_NUMERIC_FIELDS = filter(
      lambda field: isinstance(field, IntegerField) and field.name != 'id',
      Component._meta.fields
    )
    
    favorite_components = Profile.objects.get(user=self.request.user).stars.all()

    extra_context = {
      'pagename': 'Home',
      'recommended': Component.objects.all()[:20],
      'favorite_components': favorite_components,
      'modal_textual_fields': COMPONENT_TEXT_FIELDS,
      'modal_numeric_fields': COMPONENT_NUMERIC_FIELDS
    }

    return context | extra_context | self.form_data

class FavoritesView(HomeView):
  def get_queryset(self):
    queryset = super().get_queryset()
    p = Profile.objects.get(user = self.request.user)
    return queryset.filter(stars=p)
  
  def get_context_data(self, **kwargs):
    return super().get_context_data(**kwargs) | {'pagename': 'Favorites'}

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
  DestroyModelMixin):
  queryset = Component.objects.all()
  serializer_class = ComponentSerializer

  def partial_update(self, request: Request, *args, **kwargs):
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
      Request.objects.create(
        profile=Profile.objects.get(user=self.request.user),
        component=component,
        date=timezone.now(),
        quantity=requested_quantity
      )
      action = 'request'

    state = {
      'quantity': requested_quantity,
      'action': action
    }
    return Response(status=status.HTTP_200_OK, data=state)