import csv

from django.db.models import Q, F, Value, CharField

from datetime import datetime
from catalog.models import Category, SubCategory, SubCategoryKeywords
from catalog.common import RecordTypes
from accounts.models import Wallet, Profile
from finances.models import PersonalWalletRecord, GroupWalletRecord


FALLBACK_EXPENSE_CATEGORY = "Expense Other"
FALLBACK_SUBCATEGORY = "Other"

TRICOUNT_CATEGORY_MAPPING = {
    "Transport": "Transport",
    "Shopping": "Shopping",
    "Restaurants & Bars": "Food and Drinks",
    "Rent & Charges": "Household and Services",
    "Groceries": "Food and Drinks",
    "Entertainment": "Leisure",
}


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


def read_csv_file_into_dict(csv_file_path, delimiter=';'):
    # should be checked for existence before the call of this function
    list_of_dicts = []
    with open(csv_file_path, encoding='utf-8-sig') as csv_file:
        csv_reader_dict = csv.DictReader(csv_file, delimiter=delimiter)
        for row in csv_reader_dict:
            list_of_dicts.append(row)

    return list_of_dicts


def process_profile(name_string):
    lookup_string = name_string.lower().split()
    profile = Profile.objects.filter(Q(username__in=lookup_string) | Q(first_name__in=lookup_string) |
                                     Q(last_name__in=lookup_string))
    if profile.exists():
        return profile.last()  # should be one, if not make this thing smarter

    return False


def process_imported_data(csv_dict, wallet_id):
    wallet = Wallet.objects.get(id=wallet_id)

    if wallet.is_group_wallet:
        process_group_wallet_data(csv_dict, wallet)

    if wallet.is_personal_wallet:
        process_personal_wallet_data(csv_dict, wallet)


def process_personal_wallet_data(csv_dict, wallet):
    for data in csv_dict:
        try:
            date = datetime.strptime(data["Booking date"], "%Y/%m/%d")
        except ValueError:
            continue

        title = data['Title']
        amount = data["Amount"].replace(",", ".")
        if "-" in amount:
            record_type = RecordTypes.EXPENSE
            amount = amount.replace("-", "")
        else:
            record_type = RecordTypes.INCOME

        sub_category = find_sub_category(title)
        user = wallet.users.last()  # with personal wallet there is only one user
        record_data = {
            "title": title,
            "amount": amount,
            "date": date,
            "record_type": record_type,
            "personal_wallet": wallet,
            "user": user,
            "sub_category": sub_category,
            "import_confirmed": False if sub_category.parent.name == FALLBACK_EXPENSE_CATEGORY else True,
        }
        PersonalWalletRecord.objects.create(**record_data)


def process_group_wallet_data(csv_dict, wallet):
    for data in csv_dict:
        paid_by = data['Paid by']
        if paid_by is None:
            continue

        tricount_date = data["Date & time"]
        date = datetime.strptime(tricount_date, "%d/%m/%Y %H:%M").date()
        paid_by = process_profile(paid_by)
        tricount_category = data['Category']
        title = data['Title']
        sub_category = find_sub_category(title, tricount_category)
        record_data = {
            "title": title,
            "amount": data["Amount"],
            "date": date,
            "paid_by": paid_by,
            "group_wallet": wallet,
            "sub_category": sub_category,
            "import_confirmed": False if sub_category.parent.name == FALLBACK_EXPENSE_CATEGORY else True,
        }
        group_wallet_record = GroupWalletRecord.objects.create(**record_data)
        for user in wallet.users.all():
            group_wallet_record.paid_for_users.add(user)


def find_sub_category(title, tricount_category=None):
    keywords = SubCategoryKeywords.objects.annotate(
        title_string=Value(title, output_field=CharField())
    ).filter(title_string__icontains=F("keyword"))
    category_name = TRICOUNT_CATEGORY_MAPPING.get(tricount_category, None)

    if category_name:
        category = Category.objects.get(name=category_name)
        sub_category_ids = category.subcategory_set.values_list("id", flat=True)
        keywords.filter(sub_category_id__in=sub_category_ids)

    if len(keywords) >= 1:
        return keywords.last().sub_category  # usually should be here once

    sub_category = SubCategory.objects.get(parent__name=FALLBACK_EXPENSE_CATEGORY, name=FALLBACK_SUBCATEGORY)
    return sub_category
