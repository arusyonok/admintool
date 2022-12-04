import json

from django.views import generic as views
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from core.utils import get_category_tree, get_months
from catalog.common import RecordTypes
from collections import OrderedDict
from finances.models import PersonalWalletRecord


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
    template_name = 'statistics.html'
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
        expenses_datasets, incomes_datasets = self.datasets_for_chartj(records)
        context["expenses_datasets"] = json.dumps(expenses_datasets)
        context["incomes_datasets"] = json.dumps(incomes_datasets)

        context["expenses_by_category"] = self.grouped_by_category(records, RecordTypes.EXPENSE)
        context["incomes_by_category"] = self.grouped_by_category(records, RecordTypes.INCOME)

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

    def grouped_by_category(self, records, record_type):
        by_category = OrderedDict()
        records = records.filter(record_type=record_type)

        for rec in records:
            sub_category_name = rec.sub_category.name
            category_name = rec.sub_category.parent.name
            if category_name not in by_category.keys():
                by_category[category_name] = {
                    "id": rec.sub_category.parent.id,
                    "amount": 0,
                    "quantity": 0,
                    "per_day": 1,
                    "sub_values": {}
                }

            if ("sub_values" in by_category[category_name].keys() and
                    sub_category_name not in by_category[category_name]["sub_values"].keys()):
                by_category[category_name]["sub_values"][sub_category_name] = {
                    "id": rec.sub_category.id,
                    "amount": 0,
                    "quantity": 0,
                    "per_day": 1,
                    "values": []
                }

            by_category[category_name]["sub_values"][sub_category_name]["values"].append(rec)
            amount = by_category[category_name]["sub_values"][sub_category_name]["amount"] + int(rec.amount)
            by_category[category_name]["sub_values"][sub_category_name]["amount"] = amount

            cat_amount = by_category[category_name]["amount"] + int(rec.amount)
            by_category[category_name]["amount"] = cat_amount

            by_category[category_name]["quantity"] += 1
            by_category[category_name]["sub_values"][sub_category_name]["quantity"] += 1

            per_day = by_category[category_name]["amount"] / by_category[category_name]["quantity"]
            by_category[category_name]["per_day"] = per_day

            per_day = by_category[category_name]["sub_values"][sub_category_name]["amount"] / \
                      by_category[category_name]["sub_values"][sub_category_name]["quantity"]
            by_category[category_name]["sub_values"][sub_category_name]["per_day"] = per_day

        return by_category

    def datasets_for_chartj(self, records):
        expenses_records = records.filter(record_type=RecordTypes.EXPENSE).values("sub_category__parent__name").annotate(amount=Sum("amount"))
        incomes_records = records.filter(record_type=RecordTypes.INCOME).values("sub_category__parent__name").annotate(amount=Sum("amount"))

        expenses_datasets = self._create_dataset(expenses_records)
        income_datasets = self._create_dataset(incomes_records)

        return expenses_datasets, income_datasets

    def _create_dataset(self, records):
        records_dict = OrderedDict({rec["sub_category__parent__name"]: str(rec["amount"]) for rec in records})

        labels = list(records_dict.keys()) or []
        data = list(records_dict.values()) or []
        datasets = {
            "labels": labels,
            "datasets": [{
                "data": data
            }]
        }
        return datasets
