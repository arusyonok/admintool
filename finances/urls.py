from django.urls import re_path as url

from . import views

urlpatterns = [
    url(r'^$', views.Dashboard, name='dashboard'),
    url(r'dashboard', views.Dashboard, name='dashboard'),
    url(r'transactions', views.Transactions, name='transactions'),
    url(r'categories', views.Categories, name='categories'),
    url(r'trends', views.Trends, name='trends'),
]