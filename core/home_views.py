from curses.panel import update_panels
from statistics import quantiles
from django.db.models import CharField, TextField, IntegerField
from django.views.generic.list import ListView
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