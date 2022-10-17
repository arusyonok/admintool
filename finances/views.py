from django.views import generic as views
from django.urls import reverse_lazy
from catalog.common import RecordTypes
from catalog.models import Category
from core.views import BasicViewOptions
from .models import PersonalWalletRecord
from . import forms


class PersonalRecordView(BasicViewOptions, views.TemplateView):
    record_type = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['records'] = PersonalWalletRecord.objects.filter(type=self.record_type, user=self.request.user).last()
        context['header_title'] = self.header_title
        return context


class ExpenseView(PersonalRecordView):
    template_name = 'finances/personal_records/expenses.html'
    record_type = RecordTypes.EXPENSE
    header_title = "Personal Expenses"


class IncomeView(PersonalRecordView):
    template_name = 'finances/personal_records/incomes.html'
    record_type = RecordTypes.INCOME
    header_title = "Personal Incomes"


class PersonalRecordCreateView(BasicViewOptions, views.CreateView):
    model = PersonalWalletRecord
    record_type = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(type=self.record_type)
        context['header_title'] = self.header_title
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PersonalRecordCreateView, self).form_valid(form)


class ExpenseCreateView(PersonalRecordCreateView):
    form_class = forms.ExpenseCreateForm
    template_name = 'finances/personal_records/expense_add.html'
    success_url = reverse_lazy("personal-expenses")
    record_type = RecordTypes.EXPENSE
    header_title = "Add Expense"


class IncomeCreateView(PersonalRecordCreateView):
    form_class = forms.IncomeCreateForm
    template_name = 'finances/personal_records/income_add.html'
    success_url = reverse_lazy("personal-incomes")
    record_type = RecordTypes.INCOME
    header_title = "Add Income"


class PersonalRecordUpdateView(BasicViewOptions, views.UpdateView):
    model = PersonalWalletRecord
    record_type = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(type=self.record_type)
        context['parent_category'] = self.object.category
        context['header_title'] = self.header_title
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PersonalRecordUpdateView, self).form_valid(form)


class ExpenseUpdateView(PersonalRecordUpdateView):
    form_class = forms.ExpenseUpdateForm
    template_name = 'finances/personal_records/expense_edit.html'
    success_url = reverse_lazy("personal-expenses")
    record_type = RecordTypes.EXPENSE
    header_title = "Edit Expense"


class IncomeUpdateView(PersonalRecordUpdateView):
    form_class = forms.IncomeUpdateForm
    template_name = 'finances/personal_records/income_edit.html'
    success_url = reverse_lazy("personal-incomes")
    record_type = RecordTypes.INCOME
    header_title = "Edit Income"


class PersonalRecordDeleteView(BasicViewOptions, views.DeleteView):
    model = PersonalWalletRecord


class ExpenseDeleteView(PersonalRecordDeleteView):
    success_url = reverse_lazy("personal-expenses")


class IncomeDeleteView(PersonalRecordDeleteView):
    success_url = reverse_lazy("personal-incomes")


class GroupExpensesView(views.TemplateView):
    template_name = 'finances/group_expenses.html'


class GroupBalanceView(views.TemplateView):
    template_name = 'finances/group_balance.html'
