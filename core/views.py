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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context["months"] = get_months()
        context["years"] = [2021, 2022]
        context["personal_wallets"] = self.request.user.personal_wallets
        context["group_wallets"] = self.request.user.group_wallets

        active_year = self.kwargs.get("year", None)
        active_month = self.kwargs.get("month", None)
        active_personal_wallet = self.kwargs.get("personal_wallet_id", None)
        context["active_year"] = int(active_year) if active_year else None
        context["active_month"] = int(active_month) if active_month else None
        context["active_personal_wallet"] = int(active_personal_wallet) if active_personal_wallet else None

        records = self.get_records(year=active_year, month=active_month, personal_wallet=active_personal_wallet)
        expenses_datasets, incomes_datasets = self.datasets_for_chartj(records)
        context["expenses_datasets"] = json.dumps(expenses_datasets)
        context["incomes_datasets"] = json.dumps(incomes_datasets)

        return context

    def get_records(self, year=None, month=None, personal_wallet=None):
        params = {"user_id": self.request.user.id}

        if year:
            params["date__year"] = year

        if month:
            params["date__month"] = month

        if personal_wallet:
            params["personal_wallet_id"] = personal_wallet

        records = PersonalWalletRecord.objects.filter(**params)

        return records

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
