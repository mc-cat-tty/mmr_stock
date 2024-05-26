from tkinter import CASCADE
from django.db import models

class Component(models.Model):
  """
  Entity that models an electronic component; not a single instance,
  but a "model" of component.
  The composed attribute (row, column, depth) identifies a unique location.
  Enabled protection implies that a member must require access to a DL
  before using a component.
  Whenever quantity reaches zero the queuing the queuing mechanism is enabled,
  and protection flag is therefore ignored, since a request is sent anyway.
  """
  name = models.CharField(max_length=20)
  picture = models.ImageField(blank=True)
  description = models.TextField(blank=True)
  datasheet_url = models.URLField(max_length=200, blank=True)
  quantity = models.PositiveSmallIntegerField()

  row = models.PositiveSmallIntegerField()
  column = models.PositiveSmallIntegerField()
  depth = models.PositiveSmallIntegerField()

  protection = models.BooleanField(default=False, blank=True)

class User(models.Model):
  """
  Entity that models a user.
  """
  name = models.CharField(max_length=20)
  propic = models.ImageField(blank=True)

class Restriction(models.Model):
  """
  Entity that models a usage limition.
  The restriction can be absolute or periodic (i.e. after a certain period,
  the restriction resets, and the availability becomes equal to quantity again).
  Indeed, if reset_period is null, the restriction is absolute, otherwise
  the restriction becomes a "usage throttling".
  """
  class Meta:
    ordering = ['-date']
  component = models.ForeignKey(Component, on_delete=models.CASCADE)
  quantity = models.PositiveSmallIntegerField()
  date = models.DateTimeField()
  reset_period = models.DurationField(null=True, blank=True)

class Request(models.Model):
  """
  Relationship between user and component that models an enqueued request
  for a protected or out-of-stock component.
  If processed is false, the request is waiting to be processed; it can
  live as a Request.
  When processed becomes true, there are two possible outcomes.
  If processed true and the request is approved, the object is handed off to
  the Use relationship. If processed true and the request is not approved,
  it remains in Request relationship as log of failed request.
  """
  class Meta:
    ordering = ["-date", "user"]
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  component = models.ForeignKey(Component, on_delete=models.CASCADE)
  date = models.DateTimeField()
  processed = models.BooleanField(default=False, blank=True)

class Use(models.Model):
  """
  Relationship between user and component that models a use of the
  component.
  """
  class Meta:
    ordering = ["-date"]
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  component = models.ForeignKey(Component, on_delete=models.CASCADE)
  date = models.DateTimeField()
