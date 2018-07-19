from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.urls import reverse


# Create your views here.
from books.models import Book
from books.views import filter_books, detail
from vendors.forms import BookForm


def vendor_books(request, active_books=True):
    if request.user.is_authenticated:
        if request.user.member.vendor:
            queryset_paginator, page_var, genres, authors, active_books = filter_books(request,
                                                                                       vendor_filter=True,
                                                                                       active_books=active_books)
            return render(request, "vendor_home.html", {"vendor": request.user.member.vendor,
                                                        "books": queryset_paginator,
                                                        "page_var": page_var,
                                                        "genres": genres,
                                                        "authors": authors,
                                                        "active_books": active_books})
        else:
            return HttpResponseRedirect(reverse("vendors:register"))
    else:
        return HttpResponseRedirect(reverse("members:login"))


def home(request):
    return vendor_books(request)


def inactive(request):
    return vendor_books(request, active_books=False)


def register(request):

    # Create vendor_register form

    return render(request, "vendor_register.html", {})


def authenticate_member_as_vendor(request):
    pass


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)

    if request.user.is_authenticated and request.user.member.vendor == book.vendor:
        return detail(request, slug, True)
    else:
        raise PermissionDenied


def edit(request, slug):
    book = get_object_or_404(Book, slug=slug)

    if request.user.is_authenticated and request.user.member.vendor == book.vendor:

        book_form = BookForm(request.POST or None, request.FILES or None, instance=book)

        if request.method == 'POST':
            if book_form.is_valid():
                new_book = book_form.save()

                return HttpResponseRedirect(reverse("vendors:detail", kwargs={"slug": new_book.slug}))

        return render(request, "vendor_edit.html", {"book": book,
                                                    "book_form": book_form})
    else:
        raise PermissionDenied


def add(request):
    if request.user.is_authenticated and request.user.member.vendor:
        book_form = BookForm(request.POST or None, request.FILES or None)

        if request.method == 'POST':
            if book_form.is_valid():
                new_book = book_form.save(commit=False)
                new_book.vendor = request.user.member.vendor
                new_book.save()
                book_form.save_m2m()

                return HttpResponseRedirect(reverse("vendors:detail", kwargs={"slug": new_book.slug}))

        return render(request, "vendor_add_book.html", {"book_form": book_form})
    else:
        raise PermissionDenied


def delete_book(request, slug):
    book = get_object_or_404(Book, slug=slug)

    if request.user.is_authenticated and request.user.member.vendor == book.vendor:
        confirmation = request.POST.get('confirmation')

        if confirmation == "Yes, I want to delete " + book.name + ".":
            book.is_active = False
            book.save()
            return HttpResponseRedirect(reverse('vendors:vendor'))
        else:
            return render(request, "vendor_delete_book.html", {"book": book})
    else:
        raise PermissionDenied


def reactivate_book(request, slug):
    book = get_object_or_404(Book, slug=slug)

    if request.user.is_authenticated and request.user.member.vendor == book.vendor:
        book.is_active = True
        book.save()
        return HttpResponseRedirect(reverse('vendors:detail', kwargs={"slug": book.slug}))
    else:
        return render(request, "vendor_delete_book.html", {"book": book})