from django.shortcuts import render


# Create your views here.

# TEMPORARY VIEWS FOR DELIVERABLE 4


def send_page(request, slug):
    return render(request, slug + ".html", {})
