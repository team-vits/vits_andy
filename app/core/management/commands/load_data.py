from cgitb import handler
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from core.models import Exercises
import csv


def insert_exercises_data(data: dict) -> None:
    """Insert data from csv file to exercise table"""
    for row in data:
        try: 
            exercise = Exercises(**row)
            exercise.save()
        except Exception as e:
            #print({"ERROR": f"method {insert_excersices_data.__name__}, msg={e}"})
            raise e

class Command(BaseCommand):
    """Django command to wait for database."""

    def add_arguments(self, parser):
        parser.add_argument('-file', nargs='+', type=str, )

    def handle(self, *args, **options):
        """Entrypoint for command."""
        file = options['file']
        if not file:
            try:
                with open('/app/core/management/commands/exercises.csv') as csv_file:
                    data = csv.DictReader(csv_file)
                    insert_exercises_data(data)
            except Exception as e:
               # print({"ERROR": f"method {handle.__name__}, msg={e}"})
                raise e
