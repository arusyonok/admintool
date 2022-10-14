from django.views import generic as views


class HeaderClass:
    header_title = None


class MainView(views.TemplateView, HeaderClass):
    template_name = 'finances/dashboard.html'
    header_title = "Dashboard"
