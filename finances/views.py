from django.views import generic as views
from django.urls import reverse_lazy
from django.http import Http404
from accounts.models import Wallet
from catalog.common import RecordTypes
from catalog.models import Category
from core.views import BasicViewOptions
from .models import PersonalWalletRecord
from . import forms


class WalletViewDetails:
    wallet = None

    def get_wallet_or_404(self):
        wallet_pk = self.kwargs.get("wallet_pk")
        try:
            # TODO: Make this nicer error handling
            wallet = Wallet.objects.get(pk=wallet_pk, users=self.request.user)
            if not wallet.is_personal_wallet:
                raise Wallet.DoesNotExist
        except Wallet.DoesNotExist:
            raise Http404("No Wallet matches the given query.")

        return wallet


class PersonalRecordView(BasicViewOptions, views.TemplateView, WalletViewDetails):
    record_type = None

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


class GroupExpensesView(views.TemplateView):
    template_name = 'finances/group_expenses.html'


class GroupBalanceView(views.TemplateView):
    template_name = 'finances/group_balance.html'
