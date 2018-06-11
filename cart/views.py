from django.shortcuts import render

# Create your views here.


def cart(request):
    return render(request, "cart.html", {})


def checkout(request):
    return render(request, "checkout.html", {})

# Order model is used to aid Cart and Member
