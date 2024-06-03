from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from core.models import Component, Profile


class StarAPI(viewsets.ViewSet):
  permission_classes = [IsAuthenticated]
  COMPONENT_PK_KEY: str = 'component_pk'

  def toggle_star(self, request: Request) -> Response:
    try:
      component_pk = int(request.data[self.COMPONENT_PK_KEY])
    except:
      return Response(status=status.HTTP_400_BAD_REQUEST)

    component = get_object_or_404(Component, pk=component_pk)
    profile = get_object_or_404(Profile, user=request.user)
    isOn = profile.stars.filter(pk=component_pk).exists()
    
    if isOn: profile.stars.remove(component)
    else: profile.stars.add(component)

    response_data = {"status": not isOn}
    return Response(data=response_data, status=status.HTTP_200_OK)
  
  def create(self, request: Request) -> Response:
    return self.toggle_star(request)

  def destroy(self, request: Request) -> Response:
    return self.toggle_star(request)

