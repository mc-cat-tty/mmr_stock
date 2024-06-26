from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.core.files import File
from os.path import join

from mmr_stock.settings import BASE_DIR
from core.models import Profile

class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    PATH = join(BASE_DIR, 'media', 'samples')
    admin = User.objects.create_superuser("admin", 'pass@pass.com', "123")
    admin.save()
    admin.profile.propic.save(
      'admin',
      File(open(join(PATH, 'admin.png'), 'rb'))
    )

    user = User.objects.create_user("francesco", 'pass@pass.com', "123")
    user.save()
    user.profile.propic.save(
      'francesco',
      File(open(join(PATH, 'francesco.webp'), 'rb'))
    )

    for username in ('foo', 'bar', 'baz', 'qux'):
      user = User.objects.create_user(username, 'pass@pass.com', "123")
      user.save()
