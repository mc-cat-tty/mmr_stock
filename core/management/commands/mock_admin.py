from django.contrib.auth.models import User
from django.core.management import BaseCommand

class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    user = User.objects.create_superuser("admin", 'pass@pass.com', "123")
    user.save()