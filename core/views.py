from django.db import transaction
from django.forms import ModelForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit  import UpdateView
from django.urls import reverse_lazy
from django.forms import inlineformset_factory

from .models import Profile, User

class LoginView(LoginView):
  redirect_authenticated_user: bool = True
  next_page = reverse_lazy("core:home")
  template_name = "user/login.html"

class LogoutView(LogoutView):
  template_name = "user/logout.html"

class ProfileForm(ModelForm):
  class Meta:
    model = Profile
    fields = ("propic",)

class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ("username", "first_name", "last_name", "email")

# ProfileFormSet = inlineformset_factory(User, Profile, form=ProfileForm, extra=1)

# class ProfileDetailView(LoginRequiredMixin, UpdateView):
#   model = User
#   fields = ("username",)
#   template_name = "user/profile.html"
#   success_url = "."

#   def get_context_data(self, **kwargs):
#     context = super(ProfileDetailView, self).get_context_data(**kwargs)
#     if self.request.POST:
#       context['profile'] = ProfileFormSet(self.request.POST)
#     else:
#       context['profile'] = ProfileFormSet()
#     return context
  
#   def form_valid(self, form):
#     context = self.get_context_data()
#     profile = context['profile']
#     with transaction.atomic():
#       self.object = form.save()

#       if profile.is_valid():
#         profile.instance = self.object
#         profile.save()
    
#     return super(ProfileDetailView, self).form_valid(form)

#   def get_object(self):
#     return self.request.user



class ProfileDetailView(LoginRequiredMixin, UpdateView):
  model = User
  form_class = UserForm
  template_name = "user/profile.html"
  success_url = "."

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    if self.request.method == "POST":
      context['profileform'] = ProfileForm(self.request.POST)
    else:
      context['profileform'] = ProfileForm()
    return context
  
  def form_valid(self, form):
    context = self.get_context_data()
    profile = context.get('profileform')
    if profile.is_valid():
      print(profile.cleaned_data['propic'])
    #   profile.instance = self.object
    #   profile.save()
  
    return super().form_valid(form)

  def get_object(self):
    return self.request.user
  
  