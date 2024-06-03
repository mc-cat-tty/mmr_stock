from django.db.models import CharField, TextField, IntegerField, BooleanField
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from functools import reduce
import operator

from .models import *

from analytics.recommendation import get_suggested_items

class HomeView(ListView):
  model = Component
  template_name="home.html"
  paginate_by = 24
  form_data = {}
  
  def get_queryset(self):
    queryset = super().get_queryset()

    query = self.request.GET.get('query', '')
    
    # Trying to imitate full text search. Not supported by SQLite
    splitted_query = query.split()
    conditions_gen = (Q(name__icontains=word) for word in splitted_query)
    ft_query = reduce(operator.and_, conditions_gen, Q())

    queryset = queryset.filter(code__icontains=query) | queryset.filter(ft_query)
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
    COMPONENT_BOOLEAN_FIELDS = filter(
      lambda field: isinstance(field, BooleanField),
      Component._meta.fields
    )
    
    favorite_components = {}
    if self.request.user.is_authenticated:
      favorite_components = self.request.user.profile.stars.all()

    # Reccomended only for logged in users
    recommended_components = {}
    if self.request.user.is_authenticated:
      recommended_components = get_suggested_items(self.request.user.profile)

    extra_context = {
      'pagename': 'Home',
      'recommended': recommended_components,
      'favorite_components': favorite_components,
      'modal_textual_fields': list(COMPONENT_TEXT_FIELDS),
      'modal_numeric_fields': list(COMPONENT_NUMERIC_FIELDS),
      'modal_boolean_fields': list(COMPONENT_BOOLEAN_FIELDS)
    }

    return context | extra_context | self.form_data

class FavoritesView(LoginRequiredMixin, HomeView):
  def get_queryset(self):
    queryset = super().get_queryset()
    return queryset.filter(stars=self.request.user.profile)
  
  def get_context_data(self, **kwargs):
    return super().get_context_data(**kwargs) | {'pagename': 'Favorites'}
