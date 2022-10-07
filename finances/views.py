from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Transaction, TRANSACTION_TYPE_ID

def Dashboard(request):
    return render(request, 'finances/dashboard.html', {})


def Transactions(request):

    if request.GET and request.GET['type']:
        type_id = dict(TRANSACTION_TYPE_ID)[request.GET['type']]
        transactions = Transaction.objects.filter(type=type_id)
    else:
        transactions = Transaction.objects.all()

    context = {'transactions': transactions}
    return render(request, 'finances/transactions.html', context)
