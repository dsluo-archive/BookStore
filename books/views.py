import operator
import random
import string

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from books.models import Author, Book, Genre, PromotionCodes

def landing(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("books:home"))
    else:
        return HttpResponseRedirect(reverse("members:login"))


def home(request):
    new_books = Book.objects.all().order_by("-publish_date")[:4]
    latest_authors = Author.objects.all().order_by('-id')
    genres = Genre.objects.all()

    authors_to_home = []
    for author in latest_authors:
        if len(author.book_set.all()) > 0:
            authors_to_home.append(author)
    authors_to_home = authors_to_home[:4]

    genres_to_home = []
    for genre in genres:
        if len(genre.book_set.all()) > 0:
            genres_to_home.append(genre)
    genres_to_home = genres_to_home[:4]

    return render(request, "home_page.html", {
        "new_books":         new_books,
        "latest_authors":    authors_to_home,
        "genres":            genres_to_home
    })


def filter_books(request, vendor_filter, active_books=True):
    if vendor_filter:
        queryset_list = Book.objects.all().filter(vendor=request.user.member.vendor).filter(is_active=active_books)
    else:
        queryset_list = Book.objects.all().filter(is_active=True)

    search = request.GET.get('q')
    book_author = request.GET.get('author')
    book_genre = request.GET.get('genre')

    zero_to_ten = request.GET.get('zero_to_ten')
    ten_to_twenty = request.GET.get('ten_to_twenty')
    twenty_to_thirty = request.GET.get('twenty_to_thirty')
    thirty_plus = request.GET.get('thirty_plus')

    if search:
        queryset_list = queryset_list.filter(
            Q(name__icontains=search) |
            Q(author__name__icontains=search) |
            Q(isbn__exact=search) |
            Q(subjects__subjects__iexact=search)
        ).distinct()

    if book_author:
        queryset_list = queryset_list.filter(author__name=book_author)
    if book_genre:
        queryset_list = queryset_list.filter(subjects__subjects__iexact=book_genre)

    queryset = []
    entered = False
    if zero_to_ten:
        entered = True
        queryset.extend(queryset_list.filter(price__lte=10))
    if ten_to_twenty:
        entered = True
        queryset.extend(queryset_list.filter(price__lte=20).filter(price__gt=10))
    if twenty_to_thirty:
        entered = True
        queryset.extend(queryset_list.filter(price__lte=30).filter(price__gt=20))
    if thirty_plus:
        entered = True
        queryset.extend(queryset_list.filter(price__gt=30))

    if not entered:
        queryset = list(queryset_list)

    genres = []
    authors = []
    for book in queryset:
        genres.extend(book.subjects.all())
        authors.append(book.author)

    genres = sorted(list(set(genres)), key=operator.attrgetter('subjects'))
    authors = sorted(list(set(authors)), key=operator.attrgetter('name'))
    queryset = sorted(queryset, key=operator.attrgetter('name'))

    paginator = Paginator(queryset, 10)
    page_var = 'page'

    page = request.GET.get(page_var)
    queryset_paginator = paginator.get_page(page)

    return queryset_paginator, page_var, genres, authors, active_books


def all_books(request):
    queryset_paginator, page_var, genres, authors, active_books = filter_books(request, vendor_filter=False)

    return render(request, "query.html", {"books":        queryset_paginator,
                                          "page_var":     page_var,
                                          "genres":       genres,
                                          "authors":      authors,
                                          "active_books": active_books})


def detail(request, slug, vendor=False):
    book = get_object_or_404(Book, slug=slug)

    if book.is_active or vendor or request.user.is_staff:
        other_books = book.author.book_set.all().filter(~Q(slug=book.slug))[:5]

        add_to_cart = request.POST.get("cart")
        count = request.POST.get("count")

        if request.user.is_authenticated:
            if add_to_cart and count:
                success = request.user.member.cart.add_item(request.user.member, book, count)

                if success:
                    messages.success(request, book.name + " added to cart!")
                else:
                    messages.warning(request, book.name + " could not be added to cart. "
                                     + "Item currently has "
                                     + str(book.count_in_stock)
                                     + " items in stock.")

        else:
            add_to_cart = request.POST.get("cart")

            if add_to_cart:
                return HttpResponseRedirect(reverse('members:login'))

        return render(request, "book_detail.html", {"book":        book,
                                                    "other_books": other_books,
                                                    "vendor":      vendor})
    else:
        raise PermissionDenied


def query(request):
    return render(request, "query.html", {})


def generate_promotion():
    code = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))

    while PromotionCodes.objects.all().filter(code=code).exists():
        code = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))

    # getting genre to discount
    max_id = Genre.objects.all().order_by("-id")[0].id
    genre_id = random.randint(1, max_id)

    genre = Genre.objects.all().filter(id=genre_id).first()

    discount = round(random.uniform(0.05, .2), 2)

    new_promotion = PromotionCodes(code=code, discount=discount)
    new_promotion.save()

    new_promotion.genre = genre
    new_promotion.save()

    return new_promotion.code
