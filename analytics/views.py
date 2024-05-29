from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from core.models import Component, Profile

def favorites(request: HttpRequest) -> HttpResponse:
  context = {
    'pagename': 'Favorites',
  }

  return render(request, template_name="favorites.html", context=context)

class StarAPI(viewsets.ViewSet):
  COMPONENT_PK_KEY: str = 'component_pk'

  def toggle_star(self, request: Request) -> Response:
    try:
      component_pk = int(request.data[self.COMPONENT_PK_KEY])
      component = Component.objects.get(pk=component_pk)
    except:
      return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
      profile = Profile.objects.get(user=request.user)
      isOn = profile.stars.filter(pk=component_pk).exists()
      if isOn: profile.stars.remove(component)
      else: profile.stars.add(component)
    except:
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response_data = {"status": not isOn}
    return Response(data=response_data, status=status.HTTP_200_OK)
  
  def create(self, request: Request) -> Response:
    return self.toggle_star(request)

  def destroy(self, request: Request) -> Response:
    return self.toggle_star(request)
  
  def list(self, request: Request) -> Response:
    return Response(status=status.HTTP_200_OK)


