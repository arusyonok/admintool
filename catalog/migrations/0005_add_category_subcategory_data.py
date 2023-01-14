from django.db import migrations
from catalog.common import RecordTypes


CATEGORIES = {
    'Food and Drinks': 'Expense',
    'Transport': 'Expense',
    'Leisure': 'Expense',
    'Shopping': 'Expense',
    'Household and Services': 'Expense',
    'Health and Beauty': 'Expense',
    'Expense Other': 'Expense',
    'Work': 'Income',
    'Income Other': 'Income'
}

SUB_CATEGORIES = {
    'Food and Drinks': ['Groceries', 'Restaurants', 'Alcohol and Tobacco', 'Coffee and Snacks', 'Bars', 'Other'],
    'Transport': ['Car and Fuel', 'Flights', 'Public Transport', 'Taxi', 'Parking', 'Insurance and fees', 'Other'],
    'Leisure': ['Hobbies', 'Culture and Events', 'Sports and Fitness', 'Accommodation Vacation', 'Other'],
    'Shopping': ['Clothes and Accessories', 'Books and Games', 'Electronics', 'Hobby and Sports Equipments',
                 'Gifts', 'Other'],
    'Household and Services': ['Rent', 'Utilities', 'Insurance and fees', 'Communications', 'Services',
                               'Furniture and Decor', 'Renovation and Repairs', 'Other'],
    'Health and Beauty': ['Healthcare', 'Pharmacy', 'Beauty', 'Other'],
    'Expense Other': ['Other'],
    'Work': ['Salary'],
    'Income Other': ['Transfers', 'Trade', 'Tax Refund', 'Reimbursements']
}


def forwards(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    SubCategory = apps.get_model("catalog", "SubCategory")

    category_objs = []
    for name, cat_type in CATEGORIES.items():
        category_objs.append(Category(name=name, type=RecordTypes.DICT[cat_type]))
    Category.objects.bulk_create(category_objs)

    sub_category_objs = []
    for category_name, sub_category_list in SUB_CATEGORIES.items():
        category = Category.objects.get(name=category_name)
        for sub_category_name in sub_category_list:
            sub_category_objs.append(SubCategory(name=sub_category_name, parent=category))

    SubCategory.objects.bulk_create(sub_category_objs)


def backwards(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    SubCategory = apps.get_model("catalog", "SubCategory")
    Category.objects.all().delete()
    SubCategory.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_subcategorykeywords'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]