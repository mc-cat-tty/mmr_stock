from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from core.models import Component
from itertools import count
from pathlib import Path
import csv, os
from mmr_stock.settings import BASE_DIR

FILENAME: str = "mock_components.csv"
FILEPATH: str = os.path.join(
  Path(__file__).resolve().parent.parent,
  FILENAME
)

class Command(BaseCommand):
  help = "Populates DB with mock data from FILENAME"
  
  def handle(self, *args, **options):
    self.cleanup()
    self.populate()
  
  def cleanup(self) -> None:
    Component.objects.all().delete()
  
  def match_pic(self, name: str) -> str:
    PICS = {
      'resistenza': 'resistor.webp',
      'resistore': 'resistor.webp',
      'mosfet': 'mosfet.jpg',
      'led': 'led.jpg',
      'diodo': 'diode.jpg',
      'regolatore': 'regulator.jpg',
      'can ': 'can.webp'
    }
    for comp, pic in PICS.items():
      if comp in name.casefold():
        return pic
    
    return None
  
  def populate(self) -> None | CommandError:
    with open(FILEPATH) as mockfile:
      mockdata = csv.reader(mockfile, delimiter=',', quotechar='"')

      for (entry, r, c, d) in zip(mockdata, count(), count(), count()):
        c = Component(
          name=entry[0],
          code=entry[1],
          quantity=int(entry[2] if entry[2] else 0),
          row=r, column=c, depth=d,
        )

        pic = self.match_pic(entry[0])
        if pic:
          path = os.path.join(BASE_DIR, 'media', 'samples', self.match_pic(entry[0]))
          c.picture.save(
            'samples',
            File(open(path, 'rb'))
          )

        c.save()
    
    if Component.objects.count()<=0:
      raise CommandError("Population failed. No objects inserted in DB.")
  


