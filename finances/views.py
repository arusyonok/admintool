import json

from django.http import Http404
from django.urls import reverse_lazy
from django.views import generic as views

from accounts.models import Wallet
from catalog.common import RecordTypes, WalletType
from catalog.models import Category
from core.views import BasicViewOptions

from . import forms
from .models import GroupWalletRecord, PersonalWalletRecord
from .utils import get_balances


class WalletViewDetails:
    wallet = None
    wallet_type = None
    _is_personal_wallet_type = False
    _is_group_wallet_type = False

    def get_wallet_or_404(self):
        wallet_pk = self.kwargs.get("wallet_pk")
        self.check_wallet_type()
        try:
            # TODO: Make this nicer error handling
            wallet = Wallet.objects.get(pk=wallet_pk, users=self.request.user)
            if self._is_personal_wallet_type and not wallet.is_personal_wallet:
                raise Wallet.DoesNotExist
            if self._is_group_wallet_type and not wallet.is_group_wallet:
                raise Wallet.DoesNotExist
        except Wallet.DoesNotExist:
            raise Http404("No Wallet matches the given query.")

        return wallet

    def check_wallet_type(self):
        if self.wallet_type == WalletType.PERSONAL_WALLET:
            self._is_personal_wallet_type = True
        if self.wallet_type == WalletType.GROUP_WALLET:
            self._is_group_wallet_type = True


class PersonalRecordView(BasicViewOptions, views.TemplateView, WalletViewDetails):
    record_type = None
    wallet_type = WalletType.PERSONAL_WALLET

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet = self.get_wallet_or_404()
        context["records"] = PersonalWalletRecord.objects.filter(personal_wallet=wallet.pk,
                                                                 record_type=self.record_type, user=self.request.user)
        context['header_title'] = self.header_title
        context['wallet'] = wallet
        return context


class ExpenseView(PersonalRecordView):
    template_name = 'finances/personal_wallet/expenses.html'
    record_type = RecordTypes.EXPENSE
    header_title = "Personal Expenses"


class IncomeView(PersonalRecordView):
    template_name = 'finances/personal_wallet/incomes.html'
    record_type = RecordTypes.INCOME
    header_title = "Personal Incomes"


class PersonalRecordCreateView(BasicViewOptions, views.CreateView, WalletViewDetails):
    model = PersonalWalletRecord
    record_type = None
    success_url_prefix = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(type=self.record_type)
        context['header_title'] = self.header_title
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.personal_wallet = self.get_wallet_or_404()
        return super(PersonalRecordCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(self.success_url_prefix, args=[self.kwargs.get("wallet_pk")])


class ExpenseCreateView(PersonalRecordCreateView):
    form_class = forms.ExpenseCreateForm
    template_name = 'finances/personal_wallet/expense_add.html'
    success_url_prefix = "personal-expenses:view"
    record_type = RecordTypes.EXPENSE
    header_title = "Add Expense"


class IncomeCreateView(PersonalRecordCreateView):
    form_class = forms.IncomeCreateForm
    template_name = 'finances/personal_wallet/income_add.html'
    success_url_prefix = "personal-incomes:view"
    record_type = RecordTypes.INCOME
    header_title = "Add Income"


class PersonalRecordUpdateView(BasicViewOptions, views.UpdateView):
    model = PersonalWalletRecord
    record_type = None
    success_url_prefix = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(type=self.record_type)
        context['parent_category'] = self.object.category
        context['header_title'] = self.header_title
        return context

    def get_success_url(self):
        return reverse_lazy(self.success_url_prefix, args=[self.kwargs.get("wallet_pk")])


class ExpenseUpdateView(PersonalRecordUpdateView):
    form_class = forms.ExpenseUpdateForm
    template_name = 'finances/personal_wallet/expense_edit.html'
    success_url_prefix = "personal-expenses:view"
    record_type = RecordTypes.EXPENSE
    header_title = "Edit Expense"


class IncomeUpdateView(PersonalRecordUpdateView):
    form_class = forms.IncomeUpdateForm
    template_name = 'finances/personal_wallet/income_edit.html'
    success_url_prefix = "personal-incomes:view"
    record_type = RecordTypes.INCOME
    header_title = "Edit Income"


class PersonalRecordDeleteView(BasicViewOptions, views.DeleteView):
    model = PersonalWalletRecord
    success_url_prefix = None

    def get_success_url(self):
        return reverse_lazy(self.success_url_prefix, args=[self.kwargs.get("wallet_pk")])


class ExpenseDeleteView(PersonalRecordDeleteView):
    success_url_prefix = "personal-expenses:view"


class IncomeDeleteView(PersonalRecordDeleteView):
    success_url_prefix = "personal-incomes:view"


class GroupExpensesView(BasicViewOptions, views.TemplateView, WalletViewDetails):
    template_name = 'finances/group_wallet/expenses.html'
    header_title = "Group Expenses"
    wallet_type = WalletType.GROUP_WALLET

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet = self.get_wallet_or_404()
        context["records"] = GroupWalletRecord.objects.filter(group_wallet=wallet.pk)
        context['header_title'] = self.header_title
        context['wallet'] = wallet
        return context


class GroupExpenseCreateView(BasicViewOptions, views.CreateView, WalletViewDetails):
    model = GroupWalletRecord
    form_class = forms.GroupExpenseCreateForm
    template_name = 'finances/group_wallet/expense_add.html'
    success_url_prefix = "group-expenses:view"
    record_type = RecordTypes.EXPENSE
    header_title = "Add Group Expense"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(type=RecordTypes.EXPENSE)
        context['header_title'] = self.header_title
        return context

    def get_form_kwargs(self):
        kwargs = super(GroupExpenseCreateView, self).get_form_kwargs()
        kwargs["wallet_pk"] = self.kwargs.get("wallet_pk")
        return kwargs

    def form_valid(self, form):
        form.instance.group_wallet = self.get_wallet_or_404()
        return super(GroupExpenseCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(self.success_url_prefix, args=[self.kwargs.get("wallet_pk")])


class GroupExpenseUpdateView(BasicViewOptions, views.UpdateView, WalletViewDetails):
    model = GroupWalletRecord
    form_class = forms.GroupExpenseUpdateForm
    template_name = 'finances/group_wallet/expense_edit.html'
    success_url_prefix = "group-expenses:view"
    record_type = RecordTypes.EXPENSE
    header_title = "Edit Group Expense"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(type=RecordTypes.EXPENSE)
        context['parent_category'] = self.object.category
        context['header_title'] = self.header_title
        return context

    def get_form_kwargs(self):
        kwargs = super(GroupExpenseUpdateView, self).get_form_kwargs()
        kwargs["wallet_pk"] = self.kwargs.get("wallet_pk")
        return kwargs

    def form_valid(self, form):
        form.instance.group_wallet = self.get_wallet_or_404()
        return super(GroupExpenseUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(self.success_url_prefix, args=[self.kwargs.get("wallet_pk")])


class GroupExpenseDeleteView(BasicViewOptions, views.DeleteView):
    model = GroupWalletRecord
    success_url_prefix = "group-expenses:view"

    def get_success_url(self):
        return reverse_lazy(self.success_url_prefix, args=[self.kwargs.get("wallet_pk")])


class GroupBalanceView(BasicViewOptions, views.TemplateView):
    template_name = 'finances/group_wallet/balance.html'
    header_title = "Group Balance"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        datasets = self._create_datasets_for_chartj()
        context['header_title'] = self.header_title
        context['datasets'] = json.dumps(datasets)
        return context

    def _create_datasets_for_chartj(self):
        balances = get_balances(self.request.user.id, self.kwargs.get("wallet_pk"))

        labels = []
        positive_data = []
        negative_data = []
        for balance in balances:
            labels.append("/".join(balance.keys()))
            for name, amount in balance.items():
                if amount > 0:
                    positive_data.append(amount)
                else:
                    negative_data.append(amount)
        negative_dataset = {
            "backgroundColor": 'rgba(60, 141, 188, 0.9)',
            "data": negative_data
        }
        positive_dataset = {
            "backgroundColor": 'rgba(210, 214, 222, 1)',
            "data": positive_data
        }
        datasets = {
            "labels": labels,
            "datasets": [
                positive_dataset,
                negative_dataset,
            ]
        }
        return datasets
