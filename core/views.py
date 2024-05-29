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

    return context | extra_context

class FavoritesView(HomeView):
  def get_queryset(self):
    p = Profile.objects.get(user = self.request.user)
    return self.model.objects.filter(stars=p)
  
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