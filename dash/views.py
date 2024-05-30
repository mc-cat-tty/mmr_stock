from django.shortcuts import render
from django.views.generic.list import ListView
from core.models import *

class DashView(ListView):
  model = User
  template_name="dashboard.html"
  
  # def get_queryset(self):
  #   queryset = super().get_queryset()
  #   query = self.request.GET.get('query', '')

  #   self.form_data = {'query': query}

  #   return queryset.filter(username__icontains=query)

