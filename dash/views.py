from django.shortcuts import render
from django.views.generic.list import ListView
from core.models import *

class DashView(ListView):
  model = Profile
  template_name="dashboard.html"
  
  def get_queryset(self):
    queryset = super().get_queryset()
    query = self.request.GET.get('query', '')

    self.form_data = {'query': query}

    return queryset.filter(user__username__icontains=query)

  def get_context_data(self, **kwargs):
    ctx = super().get_context_data(**kwargs)
    return ctx | self.form_data