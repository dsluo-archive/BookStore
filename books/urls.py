from django.urls import path, re_path

from books import views as books_views

app_name = "books"

urlpatterns = [
    re_path(r'^$', books_views.landing, name='landing'),
    re_path(r'^home/$', books_views.home, name='home'),
    re_path(r'^book/$', books_views.home),
    re_path(r'^book/create-book/$', books_views.create_book, name='create'),
    re_path(r'^book/mass-create-book/$', books_views.mass_create_book, name='mass_create'),
    re_path(r'^book/(?P<slug>[\w-]+)/$', books_views.detail, name='detail'),
    re_path(r'^q/$', books_views.query, name='query'),

    # make / url pattern redirect to home/ if logged in
]
