from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import PersonalRecord

def Dashboard(request):
    return render(request, 'finances/dashboard.html', {})


def Transactions(request):
    transactions = PersonalRecord.objects.all()
    context = {'transactions': transactions}
    return render(request, 'finances/transactions.html', context)
