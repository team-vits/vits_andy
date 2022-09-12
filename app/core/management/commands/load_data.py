from typing import Union
from django.core.management.base import BaseCommand
from core.models import Excercises, Food
import csv
import os

MODEL_MAPPER = {
    'excercises': Excercises,
    'food': Food,
}


class Command(BaseCommand):
    """ BaseCommand Wrapper """
    help = '''
    Command For Storing csv data into the Django connected
    database using the provided model.
    '''

    def add_arguments(self, parser):
        parser.add_argument(
            '--file', nargs=1, type=str, required=True,
            help='Define a specific .csv file to load data to the database'
        )

    def handle(self, *args, **options):
        """Entrypoint for command."""
        file = options['file'][0]
        file_path = os.path.join(os.getcwd(), 'load_data', file)
        print("\033[94mload_data\033[m command reading files:")
        print(f"🔍 Using \033[94m{file_path}\033[m as file's location.")
        model = self.get_model(file)
        try:
            with open(file_path) as csv_file:
                data = csv.DictReader(csv_file)
                self.insert_data(data, model)
            print(f"✔️ Succesfully stored \033[92m{file}\033[m data into DB\n")
        except FileNotFoundError as e:
            print(f"💔 \033[91m{e}\033[m 💔\n")
            raise e

    def get_model(self, file: str) -> Union[Excercises, Food]:
        file_name = file.split('.csv')[0]
        try:
            model = MODEL_MAPPER[file_name]
            return model
        except KeyError as e:
            msg = (
                f"💔 \033[91mInvalid file name 💔\033[m"
                f"You can use {list(MODEL_MAPPER.keys())}"
            )
            print(msg)
            raise e

    def insert_data(self, data: dict, model: Union[Excercises, Food]) -> None:
        """Insert data from csv file to exercise table"""
        for row in data:
            instance = model(**row)
            instance.save()
