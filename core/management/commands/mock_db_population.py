from tkinter.tix import COLUMN
from django.core.management.base import BaseCommand, CommandError, CommandParser
from core.models import Component
from pathlib import Path
import csv, os

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
  
  def populate(self) -> None | CommandError:
    with open(FILEPATH) as mockfile:
      mockdata = csv.reader(mockfile, delimiter=',', quotechar='"')
      for entry in mockdata:
        c = Component(
          name=entry[0],
          code=entry[1],
          quantity=int(entry[2] if entry[2] else 0),
          row=1, column=1, depth=1
        )
        c.save()
    
    if Component.objects.count()<=0:
      raise CommandError("Population failed. No objects inserted in DB.")
  


