from django.shortcuts import render
from rest_framework import serializers, viewsets
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.db.models import CharField, TextField, IntegerField
from .models import Component, Profile
from django.views.generic.list import ListView

class HomeView(ListView):
  model = Component
  template_name="home.html"
  form_data = {}
  
  def get_queryset(self):
    queryset = super().get_queryset()

    query = self.request.GET.get('query', '')
    try:
      min_quantity = int(self.request.GET.get('min', 0))
    except:
      min_quantity = 0

    self.form_data = {
      'min_quantity': min_quantity,
      'query': query
    }

    return (
      queryset.filter(code__icontains=query)
      | queryset.filter(name__icontains=query)
    ).filter(quantity__gte=min_quantity)

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

class ComponentAPI(viewsets.ModelViewSet):
  queryset = Component.objects.all()
  serializer_class = ComponentSerializer    