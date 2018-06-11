from django.urls import path, re_path

from client import views as client_views

app_name = "client"

urlpatterns = [
    re_path(r'^eod-report/$', client_views.eod_rep, name='eod'),
    re_path(r'^inventory/$', client_views.inventory, name='inventory'),
    re_path(r'^book-sales/$', client_views.book_sales, name='book_sales'),
    # re_path(r'^publisher-sales/$', client_views.pub_sales, name='pub_sales'),
    # make / url pattern that redirects to current day's End Of Sales Report
]