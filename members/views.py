from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User

# Create your views here.

from members.models import Member


def profile(request, slug):
    return render(request, "user_profile.html", {"slug": slug})


def create(request):
    return render(request, "create_account.html", {})


def default_profile(request):
    slug = "Current Member's slug"
    return profile(request, slug)
