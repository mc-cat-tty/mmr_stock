from urllib import request
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from os.path import join

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
  if created:
    Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
  instance.profile.save()

class Component(models.Model):
  """
  Entity that models an electronic component; not a single entity,
  but a "model/type" of component.
  The composed attribute (row, column, depth) identifies a unique location.
  Enabling protection implies that a member must require access to a DL
  before using a component.
  """
  class Meta:
    ordering = ["-pk"]
    constraints = [
      models.UniqueConstraint(
        fields = ("row", "column", "depth"),
        name = "unique_location"
      )
    ]
   
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

  def __str__(self):
    return f"{self.pk} {self.name} {self.code}"

class Profile(models.Model):
  """
  Entity that models a profile.
  These fields are added to the standard django user.
  A star is an entity that models a many to many preference (called
  'star', visually represented as a heart) relationship
  between a user and a component.
  """
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  propic = models.ImageField(
    upload_to='users_pics',
    default=join('static', 'unknown_user.png'),
    blank=True
  )
  stars = models.ManyToManyField(Component, blank=True, related_name='stars')
  requests = models.ManyToManyField(Component, through='Request', blank=True, related_name='requests')
  uses = models.ManyToManyField(Component, through='Use', blank=True, related_name='uses')

  def __str__(self):
    return f"{self.user.pk} {self.user.username}"
   
  def has_notification(self) -> bool:
    # Trick to avoid self.request.[...].exclude(request_approved = None)
    tot_num = self.requests.count()
    not_app_num = self.requests.filter(request__approved = None).count()
    app_num = tot_num - not_app_num
    read_num = self.requests.filter(request__viewed = True).count()

    return app_num != read_num

class Request(models.Model):
  """
  Relationship between user and component that models an enqueued request
  for a protected component.
  If approved is Null, the request is waiting to be processed; it can
  live as a Request.
  When approved is set, there are two possible outcomes.
  If approved true, the object is handed off to the Use relationship.
  If processed false, it remains in Request relationship as log of failed request.
  """
  class Meta:
    ordering = ["-date", "profile"]
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  component = models.ForeignKey(Component, on_delete=models.CASCADE)
  date = models.DateTimeField()
  quantity = models.PositiveSmallIntegerField()
  approved = models.BooleanField(null=True, blank=True)
  viewed = models.BooleanField(default=False)

  def is_processed(self) -> bool:
    return self.approved != None

class Use(models.Model):
  """
  Relationship between user and component that models a use of the
  component.
  """
  class Meta:
    ordering = ["-date"]
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  component = models.ForeignKey(Component, on_delete=models.CASCADE)
  date = models.DateTimeField()
  quantity = models.PositiveSmallIntegerField()

