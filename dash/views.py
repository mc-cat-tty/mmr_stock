from re import S
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpRequest
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
    return ctx | self.form_data | {'pagename': 'Dashboard'}

class DashDetailView(TemplateView):
  template_name="dashboard_detail.html"

  def get_context_data(self, **kwargs):
    id = kwargs.get('id', 0)
    return {
      'uses': ...,
      'incoming_requests': ...
    }
