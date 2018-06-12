from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User

# Create your views here.

from client.models import Client


def eod_rep(request):
    return render(request, "eod_report.html", {})


def inventory(request):
    return render(request, "inventory.html", {})


def book_sales(request):
    return render(request, "book_sales.html", {})


'''
def pub_sales(request):
    return render(request, "pub_sales.html", {})
'''
