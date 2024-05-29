from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from core.models import Component, User
from .models import Star

def favorites(request: HttpRequest) -> HttpResponse:
  context = {
    'pagename': 'Favorites',
  }

  return render(request, template_name="favorites.html", context=context)

class StarSerializer(serializers.Serializer):
  class Meta:
    model = Star
    fields = ("user", "component")

class StarAPIView(viewsets.ViewSet):
  COMPONENT_PK_KEY: str = 'component_pk'

  def create(self, request: Request):
    # user = request.user
    # User.objects.get(user)
    # Star(user=user, component=).save()

    try: component_pk = int(request.data[self.COMPONENT_PK_KEY])
    except: return Response(status=400)

    try: component = Component.objects.get(pk=component_pk)
    except: return Response(status=404)
    
    try: Star(user=request.user, component=component).save()
    except: return Response(status=500)

    return Response(status=200)
  
  def list(self, request: Request):
    queryset = Star.objects.all()
    serializer = StarSerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request: Request, pk=None):
    pass

  def destroy(self, request: Request, pk=None):
    pass
