from django.urls import re_path as url, include

from . import views


expenses_urls = [
    url(r'edit/(?P<pk>[0-9]+)/$', views.ExpenseUpdateView.as_view(), name='edit'),
    url(r'delete/(?P<pk>[0-9]+)/$', views.ExpenseDeleteView.as_view(), name='delete'),
    url(r'add', views.ExpenseCreateView.as_view(), name='add'),
    url(r'^$', views.ExpenseView.as_view(), name='view'),
]

incomes_urls = [
    url(r'edit/(?P<pk>[0-9]+)/$', views.IncomeUpdateView.as_view(), name='edit'),
    url(r'delete/(?P<pk>[0-9]+)/$', views.IncomeDeleteView.as_view(), name='delete'),
    url(r'add', views.IncomeCreateView.as_view(), name='add'),
    url(r'^$', views.IncomeView.as_view(), name='view'),
]

group_expenses_urls = [
    url(r'^$', views.GroupExpensesView.as_view(), name='view'),
]


urlpatterns = [
    url(r'personal_wallet/(?P<wallet_pk>[0-9]+)/expenses/', include((expenses_urls, "finances"), namespace="personal-expenses")),
    url(r'personal_wallet/(?P<wallet_pk>[0-9]+)/incomes/',  include((incomes_urls, "finances"), namespace="personal-incomes")),
    url(r'group_wallet/(?P<wallet_pk>[0-9]+)/expenses/', include((group_expenses_urls, "finances"), namespace='group-expenses')),
    url(r'group_wallet/(?P<wallet_pk>[0-9]+)/balance', views.GroupBalanceView.as_view(), name='group-balance')
]
