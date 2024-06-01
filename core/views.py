from django import forms
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

class LoginView(auth_views.LoginView):
  template_name: str = "login.html"
  redirect_authenticated_user: bool = True
  next_page = reverse_lazy("core:home")
