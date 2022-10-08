from django.views.generic import TemplateView


class PersonalExpenseView(TemplateView):
    template_name = 'finances/personal_expenses.html'


class PersonalIncomeView(TemplateView):
    template_name = 'finances/personal_incomes.html'


class GroupExpensesView(TemplateView):
    template_name = 'finances/group_expenses.html'


class GroupBalanceView(TemplateView):
    template_name = 'finances/group_balance.html'
