from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin


class HeaderClass:
    header_title = None


class BasicViewOptions(LoginRequiredMixin, HeaderClass):
    pass


class MainView(BasicViewOptions, views.TemplateView):
    template_name = 'finances/dashboard.html'
    header_title = "Dashboard"
