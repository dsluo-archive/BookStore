from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.core.paginator import Paginator
import random, string

# Create your views here.
from books.models import Book, Genre, Author, PromotionCodes
from books.forms import MassBookForm, BookForm
from books.tasks import cancel_promotional


def landing(request):

    new_books = Book.objects.all().order_by("publish_date")
    newly_added_books = Book.objects.all().order_by("-id")

    return render(request, "landing.html", {"new_books": new_books,
                                            "newly_added_books": newly_added_books})


def home(request):
    new_books = Book.objects.all().order_by("publish_date")
    newly_added_books = Book.objects.all().order_by("-id")
    latest_author = Author.objects.all().order_by("-id").first()
    genres = Genre.objects.all()

    return render(request, "home_page.html", {"new_books": new_books,
                                              "newly_added_books": newly_added_books,
                                              "latest_author": latest_author,
                                              "genres": genres})


def all_books(request):
    queryset_list = Book.objects.all().order_by("name")

    search = request.GET.get('q')
    # book_name = request.GET.get('name')
    # book_author = request.GET.get('author')
    # book_isbn = request.GET.get('isbn')
    # book_genre = request.GET.get('genre')

    if search:
        queryset_list = queryset_list.filter(
            Q(name__icontains=search) |
            Q(author__name__icontains=search) |
            Q(isbn__exact=search) |
            Q(subjects__subjects__iexact=search)
        ).distinct()

    '''
    Maybe use for a filter bar. Maybe JS can handle this?
    
    if book_name:
        book_name = book_name.split('%')
        for name in book_name:
            queryset_list = queryset_list.filter(name__contains=name)
    if book_author:
        book_author = book_author.split('%')
        for author in book_author:
            queryset_list = queryset_list.filter(author__name=author)
    if book_isbn:
        book_isbn = book_isbn.split('%')
        for isbn in book_isbn:
            queryset_list = queryset_list.filter(isbn=isbn)
    if book_genre:
        book_genre = book_genre.split('%')
        for genre in book_genre:
            queryset_list = queryset_list.filter(subjects__subjects=genre)
    '''

    paginator = Paginator(queryset_list, 10)
    page_var = 'page'

    page = request.GET.get(page_var)
    queryset = paginator.get_page(page)

    return render(request, "query.html", {"books": queryset,
                                          "page_var": page_var})


def detail(request, slug):
    book = get_object_or_404(Book, slug=slug)

    add_to_cart = request.POST.get("cart")
    count = request.POST.get("count")

    if request.user.is_authenticated:
        if add_to_cart and count:
            request.user.member.cart.add_item(request.user.member, book, count)
    else:
        add_to_cart = request.POST.get("cart")

        if add_to_cart:
            return HttpResponseRedirect(reverse('members:login'))

    return render(request, "book_detail.html", {"book": book})


def create_book(request):
    if request.user.is_authenticated and (request.user.member.vendor or request.user.is_staff):
        book_form = BookForm(request.POST or None, request.FILES or None)

        if book_form.is_valid():
            book_form.save()

            return render(request, "home_page.html", {})

        return render(request, "create_book.html", {"book_form": book_form})
    else:
        raise PermissionDenied


def mass_create_book(request):
    mass_book_form = MassBookForm(request.POST or None, request.FILES or None)

    if mass_book_form.is_valid():
        return render(request, "home_page.html", {})

    return render(request, "mass_create_book.html", {"mass_book_form": mass_book_form})


def query(request):
    return render(request, "query.html", {})


def generate_promotion():
    code = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))

    while PromotionCodes.objects.all().filter(code=code).exists():
        code = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))

    # getting genre to discount
    max_id = Genre.objects.all().order_by("-id")[0].id
    genre_id = random.randint(-20, max_id+1)

    if genre_id <= 0:
        genres = Genre.objects.all()
    else:
        genres = Genre.objects.all().filter(id=genre_id)

    discount = round(random.uniform(0.05, .2), 2)

    new_promotion = PromotionCodes(code=code, discount=discount)
    new_promotion.save()

    for genre in genres:
        new_promotion.genres.add(genre)

    cancel_promotional(new_promotion.code, countdown=86400)

    return new_promotion.code
