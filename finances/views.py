from django.views.generic import TemplateView, CreateView, FormView
from catalog.common import RecordTypes
from catalog.models import Category
from .models import PersonalRecord
from .forms import PersonalExpenseCreateForm


class PersonalExpenseCreateView(CreateView):
    model = PersonalRecord
    form_class = PersonalExpenseCreateForm
    template_name = 'finances/personal_expenses_add.html'
    success_url = "personal_expenses"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(type=RecordTypes.EXPENSE)
        return context


class PersonalExpenseView(TemplateView):
    template_name = 'finances/personal_expenses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expenses'] = PersonalRecord.objects.filter(type=RecordTypes.EXPENSE)
        return context


class PersonalIncomeView(TemplateView):
    template_name = 'finances/personal_incomes.html'


class GroupExpensesView(TemplateView):
    template_name = 'finances/group_expenses.html'


class GroupBalanceView(TemplateView):
    template_name = 'finances/group_balance.html'
