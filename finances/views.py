from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Transaction, Category, CATEGORY_TYPES, TRANSACTION_TYPE_ID

def Dashboard(request):
    return render(request, 'finances/dashboard.html', {})


def Transactions(request):
    categories = Category.objects.all()

    if request.GET and request.GET['type']:
        type_id = dict(TRANSACTION_TYPE_ID)[request.GET['type']]
        transactions = Transaction.objects.filter(type=type_id)
    else:
        transactions = Transaction.objects.all()

    context = {'transactions': transactions, 'categories': categories}
    return render(request, 'finances/transactions.html', context)


def Categories(request):
    categories = Category.objects.filter(is_parent=False)
    parent_categories = Category.objects.filter(parent=None)

    children = []
    ordered_list = {"Expense": {}, "Income": {}}

    for pc in parent_categories:
        for c in categories:
            if c.parent == pc.id:
                children.append(c.name)
        cat_list = {pc.name: children}
        ordered_list[dict(CATEGORY_TYPES)[pc.type]].update(cat_list)

        children = []

    return render(request, 'finances/categories.html', {"expense_cat": ordered_list["Expense"], "income_cat": ordered_list["Income"]})



def Trends(request):
    return render(request, 'finances/trends.html', {})
