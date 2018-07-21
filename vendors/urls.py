from django.urls import re_path

from vendors import views as vendor_views

app_name = "vendors"

urlpatterns = [
    re_path(r'^validation-code$', vendor_views.request_code, name='request_code'),
    re_path(r'^book/add/$', vendor_views.add_book, name='add_book'),
    re_path(r'^book/(?P<slug>[\w-]+)/edit/$', vendor_views.edit, name='edit'),
    re_path(r'^book/(?P<slug>[\w-]+)/delete/$', vendor_views.delete_book, name='delete_book'),
    re_path(r'^book/(?P<slug>[\w-]+)/reactivate/$', vendor_views.reactivate_book, name='reactivate_book'),
    re_path(r'^book/(?P<slug>[\w-]+)/$', vendor_views.book_detail, name='detail'),
    re_path(r'^register/$', vendor_views.register, name='register'),
    re_path(r'^inactive/$', vendor_views.inactive, name='inactive'),
    re_path(r'^$', vendor_views.home, name='vendor')
]
