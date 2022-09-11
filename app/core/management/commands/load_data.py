from typing import Union
from django.core.management.base import BaseCommand
from core.models import Exercises, Food
import csv
import os



MODEL_MAPPER = {
    'exercises': Exercises,
    'Food': Food,
}


class Command(BaseCommand):
    """Django command to wait for database."""

    def add_arguments(self, parser):
        parser.add_argument('--file', nargs=1, type=str, required=True, help='Define a specific .csv file to load data to the database')


    def handle(self, *args, **options):
        """Entrypoint for command."""
        file = options['file'][0]
        file_path = os.path.join( os.getcwd(), 'load_data', file)
        if os.path.exists(file_path):
            model = self.get_model(file)
            try:
                with open(file_path) as csv_file:
                    data = csv.DictReader(csv_file)
                    self.insert_data(data, model)
            except Exception as e:
                raise e
        else:
            print(f"This file doesn't exist: {file_path}, couldn't load data to database")
            return

    
    def get_model(self, file: str) -> Union[Exercises, Food]:
        file_name = file.split('.csv')[0]
        try:
            model = MODEL_MAPPER[file_name]
            return model
        except KeyError:
            print(f"This is not a valid name for the file, you can use {MODEL_MAPPER.keys()}")
            raise

    def insert_data(self, data: dict, model: Union[Exercises, Food]) -> None:
        """Insert data from csv file to exercise table"""
        for row in data:
            instance = model(**row)
            instance.save()

