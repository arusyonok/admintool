from django.urls import re_path as url

from . import views

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='login'),
    url(r'login', views.LoginView.as_view(), name='login'),
    url(r'logout', views.LogoutView.as_view(), name='logout'),
]
