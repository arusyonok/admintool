from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Dashboard, name='dashboard'),
    url(r'dashboard', views.Dashboard, name='dashboard'),
    url(r'transactions', views.Transactions, name='transactions'),
    url(r'categories', views.Categories, name='categories'),
    url(r'trends', views.Trends, name='trends'),
    url(r'budget', views.Budget, name='budget'),
]