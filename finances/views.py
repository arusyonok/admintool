from django.views import generic as views
from django.urls import reverse_lazy
from catalog.common import RecordTypes
from catalog.models import Category
from .models import PersonalRecord
from . import forms


class PersonalExpenseCreateView(views.CreateView):
    model = PersonalRecord
    form_class = forms.PersonalExpenseCreateForm
    template_name = 'finances/personal_expenses_add.html'
    success_url = "personal_expenses"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(type=RecordTypes.EXPENSE)
        return context


class PersonalExpenseUpdateView(views.UpdateView):
    model = PersonalRecord
    form_class = forms.PersonalExpenseUpdateForm
    template_name = 'finances/personal_expenses_edit.html'
    success_url = "personal_expenses"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(type=RecordTypes.EXPENSE)
        context['parent_category'] = self.object.category
        return context


class PersonalExpenseDeleteView(views.DeleteView):
    model = PersonalRecord
    success_url = reverse_lazy("personal_expenses")
    template_name = "finances/personal_expenses_delete.html"


class PersonalExpenseView(views.TemplateView):
    template_name = 'finances/personal_expenses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expenses'] = PersonalRecord.objects.filter(type=RecordTypes.EXPENSE)
        return context


class PersonalIncomeView(views.TemplateView):
    template_name = 'finances/personal_incomes.html'



class GroupExpensesView(views.TemplateView):
    template_name = 'finances/group_expenses.html'


class GroupBalanceView(views.TemplateView):
    template_name = 'finances/group_balance.html'
