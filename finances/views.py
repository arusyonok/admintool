from django.views.generic import TemplateView
from catalog.common import RecordTypes
from .models import PersonalRecord


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
