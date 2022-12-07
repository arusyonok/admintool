import json
import typing

from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from core.utils import get_category_tree, get_months
from catalog.common import RecordTypes
from collections import OrderedDict
from finances.models import PersonalWalletRecord
from dataclasses import dataclass


@dataclass
class RecordsDisplayData:
    amount: int = 0
    quantity: int = 0
    sub_values: typing.Optional[typing.Dict] = None
    values: typing.Optional[typing.List] = None

    def __post_init__(self):
        if self.sub_values and self.values:
            raise Exception("Sub Values OR Values must be set! Not Both!")
        if self.sub_values is None and self.values is None:
            raise Exception("Either/Or Sub Values or Values must be set!")


class BasicViewOptions(LoginRequiredMixin, views.base.ContextMixin):
    header_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_title'] = self.header_title
        context["user_display_name"] = self.request.user.name_display
        return context


class DashboardView(BasicViewOptions, views.TemplateView):
    template_name = 'dashboard.html'
    header_title = "Dashboard"


class CategoryView(BasicViewOptions, views.TemplateView):
    template_name = 'categories.html'
    header_title = "Categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense_categories'] = get_category_tree(category_type=RecordTypes.EXPENSE)
        context['income_categories'] = get_category_tree(category_type=RecordTypes.INCOME)
        context['transfer_categories'] = get_category_tree(category_type=RecordTypes.TRANSFER)

        return context


class StatisticsView(BasicViewOptions, views.TemplateView):
    template_name = 'statistics/main.html'
    header_title = "Statistics"
    active_month = None
    active_year = None
    active_personal_wallet = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context["months"] = get_months()
        context["years"] = [2021, 2022]
        context["personal_wallets"] = self.request.user.personal_wallets
        context["group_wallets"] = self.request.user.group_wallets

        self.active_year = int(self.kwargs.get("year")) if self.kwargs.get("year") else None
        self.active_month = int(self.kwargs.get("month")) if self.kwargs.get("month") else None
        self.active_personal_wallet = int(self.kwargs.get("personal_wallet_id")) if self.kwargs.get("personal_wallet_id") else None

        context["active_year"] = self.active_year
        context["active_month"] = self.active_month
        context["active_personal_wallet"] = self.active_personal_wallet

        records = self.get_records()

        expenses_by_category = self.grouped_by_category_for_table(records, RecordTypes.EXPENSE)
        expenses_by_cat_datasets = self.create_datasets_for_chartj(expenses_by_category)
        context["expenses_by_category"] = expenses_by_category
        context["expenses_by_cat_datasets"] = json.dumps(expenses_by_cat_datasets)

        incomes_by_category = self.grouped_by_category_for_table(records, RecordTypes.INCOME)
        incomes_datasets = self.create_datasets_for_chartj(incomes_by_category)
        context["incomes_by_category"] = incomes_by_category
        context["incomes_by_cat_datasets"] = json.dumps(incomes_datasets)

        return context

    def get_records(self):
        params = {"user_id": self.request.user.id}

        if self.active_year:
            params["date__year"] = self.active_year

        if self.active_month:
            params["date__month"] = self.active_month

        if self.active_personal_wallet:
            params["personal_wallet_id"] = self.active_personal_wallet

        records = PersonalWalletRecord.objects.filter(**params)

        return records

    def grouped_by_category_for_table(self, records, record_type):
        by_category = OrderedDict()
        records = records.filter(record_type=record_type)

        for rec in records:
            sub_category_name = rec.sub_category.name
            category_name = rec.sub_category.parent.name
            if category_name not in by_category.keys():
                by_category[category_name] = RecordsDisplayData(sub_values={})

            if (isinstance(by_category[category_name].sub_values, dict) and
                    sub_category_name not in by_category[category_name].sub_values.keys()):
                by_category[category_name].sub_values[sub_category_name] = RecordsDisplayData(values=[])

            # append record to its rightful place in the tree
            by_category[category_name].sub_values[sub_category_name].values.append(rec)

            # calculate the amounts
            sub_category_amount = by_category[category_name].sub_values[sub_category_name].amount + int(rec.amount)
            by_category[category_name].sub_values[sub_category_name].amount = sub_category_amount

            category_amount = by_category[category_name].amount + int(rec.amount)
            by_category[category_name].amount = category_amount

            # calculate quantities
            by_category[category_name].quantity += 1
            by_category[category_name].sub_values[sub_category_name].quantity += 1

        return by_category

    def create_datasets_for_chartj(self, records):
        records_dict = OrderedDict({key: values.amount for key, values in records.items()})

        labels = list(records_dict.keys()) or []
        data = list(records_dict.values()) or []
        datasets = {
            "labels": labels,
            "datasets": [{
                "data": data
            }]
        }
        return datasets
