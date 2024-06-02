from django.db import transaction
from django.forms import ModelForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit  import UpdateView
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django import forms

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
    fields = ("propic","user")

class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ("username", "first_name", "last_name", "email")

ProfilePropicFormSet = forms.models.inlineformset_factory(
    User, Profile, form=ProfileForm, can_delete=False,
    extra=0, min_num=1, validate_min=True,
)

class ProfileDetailView(LoginRequiredMixin, UpdateView):
  model = User
  form_class = UserForm
  template_name = "user/profile.html"
  success_url = "."

  def get_role(self):
    if self.request.user.is_superuser: return "admin"
    if self.request.user.is_staff: return "DL"
    else: return "member" 

  def get_context_data(self, **kwargs):
    context = super(ProfileDetailView, self).get_context_data(**kwargs)
    if self.request.POST:
      context['profileform'] = ProfilePropicFormSet(
        self.request.POST,
        self.request.FILES,
        instance=self.object
      )
    else:
      context['profileform'] = ProfilePropicFormSet(instance=self.object)
    return context | {'pagename': 'Profile', 'role': self.get_role()}
  
  def form_valid(self, form):
    context = self.get_context_data()
    profile = context.get('profileform')
    if profile.is_valid():
      self.object = form.save()
      profile.instance = self.object
      profile.save()
    else:
      return self.form_invalid(form)
  
    return super().form_valid(form)

  def get_object(self):
    return self.request.user
  
  