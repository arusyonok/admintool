from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from core.utils import get_category_tree
from catalog.common import RecordTypes


class BasicViewOptions(LoginRequiredMixin, views.base.ContextMixin):
    header_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_title'] = self.header_title
        context["user_display_name"] = self.request.user.name_display
        return context


class DashboardView(BasicViewOptions, views.TemplateView):
    template_name = 'dashboard.html'
    header_title = "Dashboard"


class CategoryView(BasicViewOptions, views.TemplateView):
    template_name = 'categories.html'
    header_title = "Categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense_categories'] = get_category_tree(category_type=RecordTypes.EXPENSE)
        context['income_categories'] = get_category_tree(category_type=RecordTypes.INCOME)
        context['transfer_categories'] = get_category_tree(category_type=RecordTypes.TRANSFER)

        return context
