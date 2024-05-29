from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from core.models import Component, Profile

def favorites(request: HttpRequest) -> HttpResponse:
  context = {
    'pagename': 'Favorites',
  }

  return render(request, template_name="favorites.html", context=context)

class StarAPIView(viewsets.ViewSet):
  COMPONENT_PK_KEY: str = 'component_pk'

  def create(self, request: Request):
    try: component_pk = int(request.data[self.COMPONENT_PK_KEY])
    except: return Response(status=400)

    try: component = Component.objects.get(pk=component_pk)
    except: return Response(status=404)
    
    profile = Profile.objects.get(user=request.user)
    profile.stars.add(component)
    # try:
    #   request.user.stars.add(component)
    # except: return Response(status=500)

    return Response(status=200)
  
  def list(self, request: Request):
    return Response(status=200)

  def retrieve(self, request: Request, pk=None):
    pass

  def destroy(self, request: Request, pk=None):
    pass
