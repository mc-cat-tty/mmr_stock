from django.db import models
from django.contrib.auth.models import User
from os.path import join

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
  name = models.CharField(max_length=300)
  code = models.CharField(max_length=50, blank=True)
  picture = models.ImageField(
    upload_to='components_pics',
    default=join('static', 'unknown_component.png'),
    blank=True
  )
  datasheet_url = models.URLField(max_length=2048, blank=True)
  quantity = models.PositiveSmallIntegerField()

  row = models.PositiveSmallIntegerField()
  column = models.PositiveSmallIntegerField()
  depth = models.PositiveSmallIntegerField()

  protection = models.BooleanField(default=False, blank=True)

class Profile(models.Model):
  """
  Entity that models a profile.
  These fields are added to the standard django user
  """
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  propic = models.ImageField(
    upload_to='users_pics',
    default=join('static', 'unknown_user.png'),
    blank=True
  )

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
