import calendar
from catalog.models import Category
from catalog.common import RecordTypes


def get_category_tree(category_type=None):
    if category_type in RecordTypes.LIST:
        category_objects = Category.objects.filter(type=category_type)
    else:
        category_objects = Category.objects.all()

    categories = {}
    for cat in category_objects:
        categories[cat.name] = []
        sub_categories = cat.subcategory_set.all()
        for sub_cat in sub_categories:
            categories[cat.name].append(sub_cat.name)

    return categories


def get_months():
    months = {}
    for i in range(1, 13):
        months[i] = calendar.month_abbr[i]

    return months
