from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    template = 'finances/dashboard.html'

    return render(request, template)
