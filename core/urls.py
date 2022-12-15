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


year_regex = "(?:year/(?P<year>[0-9]{4})/)?"
month_regex = "(?:month/(?P<month>[1-9]|1[0-2])/)?"
personal_wallet_regex = "(?:personal-wallet/(?P<personal_wallet_id>[0-9]+)/)?"
group_wallet_regex = "(?:group-wallet/(?P<group_wallet_id>[0-9]+)/)?"

filtering_url_arguments = f"{year_regex}{month_regex}{personal_wallet_regex}{group_wallet_regex}"

statistics_urls = [
    url(r'^filter/' + filtering_url_arguments, core_views.StatisticsView.as_view(), name="filter"),
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
