from django.views import generic as views
from django.urls import reverse_lazy
from catalog.common import RecordTypes
from catalog.models import Category
from .models import PersonalRecord
from . import forms


class PersonalRecordView(views.TemplateView):
    record_type = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['records'] = PersonalRecord.objects.filter(type=self.record_type)
        return context


class ExpenseView(PersonalRecordView):
    template_name = 'finances/personal_expenses.html'
    record_type = RecordTypes.EXPENSE


class IncomeView(PersonalRecordView):
    template_name = 'finances/personal_incomes.html'
    record_type = RecordTypes.INCOME


class PersonalRecordCreateView(views.CreateView):
    model = PersonalRecord
    record_type = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(type=self.record_type)
        return context


class ExpenseCreateView(PersonalRecordCreateView):
    form_class = forms.ExpenseCreateForm
    template_name = 'finances/personal_expenses_add.html'
    success_url = reverse_lazy("personal_expenses")
    record_type = RecordTypes.EXPENSE


class IncomeCreateView(PersonalRecordCreateView):
    form_class = forms.IncomeCreateForm
    template_name = 'finances/personal_incomes_add.html'
    success_url = reverse_lazy("personal_incomes")
    record_type = RecordTypes.INCOME


class PersonalRecordUpdateView(views.UpdateView):
    model = PersonalRecord
    record_type = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(type=self.record_type)
        context['parent_category'] = self.object.category
        return context


class ExpenseUpdateView(PersonalRecordUpdateView):
    form_class = forms.ExpenseUpdateForm
    template_name = 'finances/personal_expenses_edit.html'
    success_url = reverse_lazy("personal_expenses")
    record_type = RecordTypes.EXPENSE


class IncomeUpdateView(PersonalRecordUpdateView):
    form_class = forms.IncomeUpdateForm
    template_name = 'finances/personal_incomes_edit.html'
    success_url = reverse_lazy("personal_incomes")
    record_type = RecordTypes.INCOME


class PersonalRecordDeleteView(views.DeleteView):
    model = PersonalRecord


class ExpenseDeleteView(PersonalRecordDeleteView):
    success_url = reverse_lazy("personal_expenses")


class IncomeDeleteView(PersonalRecordDeleteView):
    success_url = reverse_lazy("personal_incomes")


class GroupExpensesView(views.TemplateView):
    template_name = 'finances/group_expenses.html'


class GroupBalanceView(views.TemplateView):
    template_name = 'finances/group_balance.html'
