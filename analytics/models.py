from django.db import models
from core.models import Component, User

class Star(models.Model):
  """
  Entity that models a many to many preference (called
  'star', visually represented as a heart) relationship
  between a user and a component.
  """
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  component = models.ForeignKey(Component, on_delete=models.CASCADE)