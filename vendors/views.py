import csv
from io import TextIOWrapper

from django.core.mail import send_mail
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.urls import reverse


# Create your views here.
from books.models import Author, Book, Genre, Publisher
from books.views import filter_books, detail
from vendors.forms import BookForm, VendorRegistrationForm, MassAddForm
from vendors.models import Vendor


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
    vendor_form = VendorRegistrationForm(request.POST or None)

    if request.user.is_authenticated and not request.user.member.vendor:
        if request.method == 'POST':
            if vendor_form.is_valid():

                vendor = Vendor.objects.all().filter(vendor_name=vendor_form.cleaned_data['vendor']).first()
                if vendor_form.cleaned_data['code'] == vendor.vendor_passcode:
                    request.user.member.vendor = vendor
                    request.user.member.save()
                    messages.success(request, "Successfully validatd as a member of " + vendor.vendor_name + ".")
                    return HttpResponseRedirect(reverse("vendors:vendor"))
                else:
                    messages.warning(request, "Code is invalid for this vendor.")

    return render(request, "vendor_register.html", {"vendor_form": vendor_form})


def request_code(request):
    if request.user.is_authenticated and request.user.member.vendor:
        send_mail("Vendor Authentication Code",
                  "Dog Ear Bookstore" + "\n\n"
                  + "Your authentication code is: " + request.user.member.vendor.vendor_passcode,
                  "dogearbookstore@gmail.com",
                  [request.user.email],
                  fail_silently=True)
        messages.success(request, "Verification code has been emailed to you.")
        return HttpResponseRedirect(reverse("vendors:vendor"))
    else:
        raise PermissionDenied


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


def add_book(request):
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


def mass_add(request):
    if request.user.is_authenticated and request.user.member.vendor:

        mass_add_form = MassAddForm(request.POST or None, request.FILES or None)

        if request.method == 'POST':

            if mass_add_form.is_valid():
                file = TextIOWrapper(request.FILES['csv'].file, encoding=request.encoding)
                reader = csv.DictReader(file)

                headers = reader.fieldnames
                authors = False
                genres = False
                publishers = False

                for head in headers:
                    if head == 'Authors':
                        authors = True
                    elif head == 'Genres':
                        genres = True
                    elif head == 'Publishers':
                        publishers = True

                for row in reader:
                    if authors and row['Authors']:
                        author, created = Author.objects.get_or_create(name__iexact=row['Authors'])
                        if created:
                            author.name = row['Authors']
                            author.save()
                    if genres and row['Genres']:
                        genre, created = Genre.objects.get_or_create(subjects__iexact=row['Genres'])
                        if created:
                            genre.subjects = row['Genres']
                            genre.save()
                    if publishers and row['Publishers']:
                        publisher, created = Publisher.objects.get_or_create(name__iexact=row['Publishers'])
                        if created:
                            publisher.name = row['Publishers']
                            publisher.save()

                file.close()

                return HttpResponseRedirect(reverse("vendors:vendor"))

        return render(request, "mass_add.html", {"mass_add_form": mass_add_form})
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