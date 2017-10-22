from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Transaction, Category

def Dashboard(request):
    return render(request, 'finances/dashboard.html', {})

def Transactions(request):
    transactions = Transaction.objects.all()

    return render(request, 'finances/transactions.html', {'transactions': transactions})

def Categories(request):
    categories = Category.objects.all()

    return render(request, 'finances/categories.html', {'transactions': categories})

def Trends(request):
    return render(request, 'finances/trends.html', {})

def Budget(request):
    return render(request, 'finances/budget.html', {})