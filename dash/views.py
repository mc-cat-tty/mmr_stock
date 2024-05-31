from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpRequest
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from json import dumps

from core.models import *
from core.request_views import RequestSerializer 

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
    todo = 'todo' in self.request.GET
    
    all_users = True
    username = "All Users"
    requests = Request.objects.all()
    uses = Use.objects.all()
    
    if id > 0:
      all_users = False
      profile = Profile.objects.get(user__pk=id)
      username = profile.user.username
      uses = uses.filter(profile=profile)
      requests = requests.filter(profile=profile)

    return {
      'uses': uses,
      'requests': requests.filter(approved=None) if todo else requests,
      'pagename': f'Dashboard {username}',
      'todo': todo,
      'all_users': all_users
    }

class DashUpdatesAPI(AsyncWebsocketConsumer):
  async def connect(self):
    user_id = self.scope["url_route"]["kwargs"]["user_id"]
    group_name = f"user_{user_id}"

    await self.channel_layer.group_add(
      group_name,
      self.channel_name
    )
    await self.accept()
  
  @database_sync_to_async
  def get_data(self, request_pk):
    return RequestSerializer(Request.objects.get(pk=request_pk)).data
  
  async def receive(self, text_data):
    data = await self.get_data()
    print(text_data)
    await self.send(dumps(data))
  
  async def request_update(self, event):
    request_pk = event.get("request_pk")
    request = await self.get_data(request_pk)
    await self.send(dumps(request))