from core.models import Component

def cleanup():
  Component.objects.all().delete()

def populate():
  c = Component()
  c.save()
  assert len(Component.objecs.all())>0, "Population failed"