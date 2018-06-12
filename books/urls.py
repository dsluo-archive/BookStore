from django.urls import path, re_path

from books import views as books_views

app_name = "books"

urlpatterns = [
    re_path(r'^$', books_views.landing, name='landing'),
    re_path(r'^home/$', books_views.home, name='home'),
    re_path(r'^item/(?P<slug>[\w-]+)/$', books_views.detail, name='detail'),
    re_path(r'^q/$', books_views.query, name='query'),

    # make / url pattern redirect to home/ if logged in
]
