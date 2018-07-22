from django.urls import re_path
from django.contrib.auth import settings
from django.conf.urls.static import static


from analytics import views as analytics_views

app_name = "analytics"

urlpatterns = [
    re_path(r'^end-of-day/(?P<date>[\w-]+)/$', analytics_views.eod_report, name='eod_report'),
    re_path(r'^low-inventory/$', analytics_views.low_inv_report, name='low_inv_report'),
    re_path(r'^book-sales/(?P<date>[\w-]+)/$', analytics_views.book_sales_report, name='book_sales_report'),
    re_path(r'^publisher-sales/(?P<date>[\w-]+)/$', analytics_views.publisher_sales_report, name='publisher_sales_report'),

    re_path(r'^end-of-day/$', analytics_views.eod_view, name='eod_view'),
    re_path(r'^book-sales/$', analytics_views.book_sales_view, name='book_sales_view'),
    re_path(r'^publisher-sales/$', analytics_views.publisher_sales_view, name='publisher_sales_view'),

    re_path(r'^$', analytics_views.reports_overview, name='reports_overview'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)