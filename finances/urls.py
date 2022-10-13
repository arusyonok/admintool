from django.urls import re_path as url

from . import views

urlpatterns = [
    url(r'^$', views.ExpenseView.as_view(), name='personal_expenses'),
    url(r'personal/expenses/edit/(?P<pk>[0-9]+)/$', views.ExpenseUpdateView.as_view(), name='personal_expenses_edit'),
    url(r'personal/expenses/delete/(?P<pk>[0-9]+)/$', views.ExpenseDeleteView.as_view(), name='personal_expenses_delete'),
    url(r'personal/expenses/add', views.ExpenseCreateView.as_view(), name='personal_expenses_add'),
    url(r'personal/expenses', views.ExpenseView.as_view(), name='personal_expenses'),
    url(r'personal/incomes/edit/(?P<pk>[0-9]+)/$', views.IncomeUpdateView.as_view(), name='personal_incomes_edit'),
    url(r'personal/incomes/delete/(?P<pk>[0-9]+)/$', views.IncomeDeleteView.as_view(),
        name='personal_incomes_delete'),
    url(r'personal/incomes/add', views.IncomeCreateView.as_view(), name='personal_incomes_add'),
    url(r'personal/incomes', views.IncomeView.as_view(), name='personal_incomes'),
    url(r'group/expenses', views.GroupExpensesView.as_view(), name='group_expenses'),
    url(r'group/balance', views.GroupBalanceView.as_view(), name='group_balance'),
]