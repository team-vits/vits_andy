from django.core.management.base import BaseCommand
from core.models import Excercises
import csv


def insert_excercises_data(data: dict) -> None:
    """Insert data from csv file to excercise table"""
    for row in data:
        try:
            excercise = Excercises(**row)
            excercise.save()
        except Exception as e:
            raise e


class Command(BaseCommand):
    """ BaseCommand Wrapper """
    help = '''
    Command For Storing csv data into the Django connected
    database using the provided model.
    '''

    def add_arguments(self, parser):
        path = '/app/core/management/commands/excercises.csv'
        parser.add_argument('--file', default=path)

    def handle(self, *args, **options):
        """Entrypoint for command."""
        path = options['file']
        try:
            with open(path) as csv_file:
                data = csv.DictReader(csv_file)
                insert_excercises_data(data)
        except FileNotFoundError as e:
            print(f"\033[91m{e}\033[m")
            exit
