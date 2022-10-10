from django.urls import re_path as url

from . import views

urlpatterns = [
    url(r'^$', views.PersonalExpenseView.as_view(), name='personal_expenses'),
    url(r'personal/expenses/add', views.PersonalExpenseCreateView.as_view(), name='personal_expenses_add'),
    url(r'personal/expenses', views.PersonalExpenseView.as_view(), name='personal_expenses'),
    url(r'personal/incomes', views.PersonalIncomeView.as_view(), name='personal_incomes'),
    url(r'group/expenses', views.GroupExpensesView.as_view(), name='group_expenses'),
    url(r'group/balance', views.GroupBalanceView.as_view(), name='group_balance'),
]