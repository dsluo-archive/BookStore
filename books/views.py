from django.shortcuts import render

# Create your views here.
from books.models import Book


def landing(request):
    return render(request, "landing.html", {})


def home(request):
    return render(request, "home_page.html", {})


def detail(request, slug):
    return render(request, "book_detail.html", {"slug": slug})


def query(request):
    return render(request, "query.html", {})
