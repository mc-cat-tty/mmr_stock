from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from core.models import Component

def favorites(request: HttpRequest) -> HttpResponse:
  context = {
    'pagename': 'Favorites',
    'starred': Component.objects.all()
  }

  return render(request, template_name="favorites.html", context=context)
