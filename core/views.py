from django import forms
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class LoginView(LoginView):
  redirect_authenticated_user: bool = True
  next_page = reverse_lazy("core:home")

# Forwarding vanilla LogoutView
from django.contrib.auth.views import LogoutView