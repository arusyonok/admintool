from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin


class HeaderClass:
    header_title = None


class BasicViewOptions(LoginRequiredMixin, HeaderClass):
    pass


class DashboardView(BasicViewOptions, views.TemplateView):
    template_name = 'dashboard.html'
    header_title = "Dashboard"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_title'] = self.header_title
        context["user_display_name"] = self.request.user.name_display
        return context
