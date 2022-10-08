import csv
import os
from core.settings import BASE_DIR
from django.core.management.base import BaseCommand
from catalog.models import Category, SubCategory
from catalog.common import RecordTypes

FILEPATH = os.path.join(BASE_DIR, "assets/category_types.csv")


class Command(BaseCommand):

    @staticmethod
    def _read_file():
        category_data = {}
        sub_category_data = []

        with open(FILEPATH) as file:
            reader = csv.reader(file)
            for row in reader:
                category_data[row[0]] = row[2]
                sub_category_data.append({
                    "category": row[0],
                    "sub_category_name": row[1],
                })

        return category_data, sub_category_data

    def handle(self, *args, **options):
        category_data, sub_category_data = self._read_file()
        import pdb
        pdb.set_trace()
        self._create_categories(category_data)
        self._create_sub_categories(sub_category_data)

    @staticmethod
    def _create_categories(category_data):
        new_objs = []
        for name, type in category_data.items():
            new_objs.append(Category(name=name, type=RecordTypes.DICT[type]))
        Category.objects.bulk_create(new_objs)


    @staticmethod
    def _create_sub_categories(sub_category_data):
        new_objs = []
        for data in sub_category_data:
            category = Category.objects.get(name=data['category'])
            new_objs.append(SubCategory(name=data['sub_category_name'], parent=category))

        SubCategory.objects.bulk_create(new_objs)
