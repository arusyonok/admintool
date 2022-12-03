"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path as url, include
from django.contrib import admin
from core import views as core_views


statistics_urls = [
    url(r'^personal-wallet-(?P<personal_wallet_id>[0-9]+)/year-(?P<year>[0-9]{4})/month-(?P<month>[0-9]+)/$',
        core_views.StatisticsView.as_view(), name="personal-wallet-year-month"),
    url(r'^personal-wallet-(?P<personal_wallet_id>[0-9]+)/year-(?P<year>[0-9]{4})/$',
        core_views.StatisticsView.as_view(), name="personal-wallet-year"),
    url(r'^personal-wallet-(?P<personal_wallet_id>[0-9]+)/month-(?P<month>[0-9]+)/$',
        core_views.StatisticsView.as_view(), name="personal-wallet-month"),
    url(r'^year-(?P<year>[0-9]{4})/month-(?P<month>[0-9]+)/$',
        core_views.StatisticsView.as_view(), name="year-month"),
    url(r'^year-(?P<year>[0-9]{4})/$',
        core_views.StatisticsView.as_view(), name="year"),
    url(r'^month-(?P<month>[0-9]+)/$',
        core_views.StatisticsView.as_view(), name="month"),
    url(r'^personal-wallet-(?P<personal_wallet_id>[0-9]+)/$',
        core_views.StatisticsView.as_view(), name="personal-wallet"),
    url(r'^$', core_views.StatisticsView.as_view(), name='view'),
]

urlpatterns = [
    url(r'^$', core_views.DashboardView.as_view(), name='dashboard'),
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard', core_views.DashboardView.as_view(), name='dashboard'),
    url(r'^categories', core_views.CategoryView.as_view(), name='categories'),
    url(r'^statistics/',  include((statistics_urls, "statistics"), namespace="statistics")),
    url(r'^finances/', include('finances.urls')),
    url(r'^accounts/', include('accounts.urls')),
]
