from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from books.models import Book


# Create your views here.


def cart(request):
    if request.user.is_anonymous:
        return render(request, "cart.html", {"cart_items": []})
    else:
        return render(request, "cart.html", {"cart_items": request.user.member.cart.items.all()})


def remove(request, slug):
    book = Book.objects.all().filter(slug=slug).first()
    request.user.member.cart.cancel_purchase(request.user.member, book)

    return HttpResponseRedirect(reverse('cart:cart'))


def checkout(request):
    return render(request, "checkout.html", {})

# Order model is used to aid Cart and Member
