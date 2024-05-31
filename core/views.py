from django import forms
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login

class LoginForm(forms.Form):
  username = forms.CharField(required=True)
  password = forms.CharField(widget=forms.PasswordInput, required=True)

def login_view(request: HttpRequest) -> HttpResponse:
  if request.method == "POST":
    form = LoginForm(request.POST)
    if not form.is_valid(): render(request, "login.html", {'form': form})
    username = form.cleaned_data["username"]
    password = form.cleaned_data["password"]
    user = authenticate(request, username=username, password=password)
    if not user: return render(request, "login.html", {'form': form})
    login(request, user)
    return redirect("core:home")

  form = LoginForm()  
  return render(request, "login.html", {'form': form})