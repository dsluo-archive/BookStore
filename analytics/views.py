from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from analytics.models import EodReport, LowInvReport, BookSalesReport, PublisherSalesReport
# Create your views here.


def eod_report(request, date):
    if request.user.is_authenticated and request.user.member.is_client:
        report = EodReport.objects.all().filter(date=date).first()
        return render(request, "eod_report.html", {"report": report})
    else:
        raise PermissionDenied


def low_inv_report(request):
    if request.user.is_authenticated and request.user.member.is_client:
        report = LowInvReport.objects.first()
        return render(request, "inventory.html", {"report": report})
    else:
        raise PermissionDenied


def book_sales_report(request, date):
    if request.user.is_authenticated and request.user.member.is_client:
        report = BookSalesReport.objects.all().filter(date=date).first()

        books = {}
        for item in report.book.all():
            if item.book.slug in books:
                books.update({item.book: (item.count + books.get(item.book.slug)[0],
                                               books.get(item.book.slug)[0] + float(item.count * item.price))})
            else:
                books.update({item.book: (item.count, float(item.count * item.price))})

        return render(request, "book_sales.html", {"report": report,
                                                   "books": books})
    else:
        raise PermissionDenied


def publisher_sales_report(request, date):
    if request.user.is_authenticated and request.user.member.is_client:
        report = PublisherSalesReport.objects.all().filter(date=date).first()

        publishers = {}
        for item in report.publisher.all():
            if item.book.publisher in publishers:
                publishers.update({item.book.publisher: (item.count + publishers.get(item.book.publisher)[0],
                                                         publishers.get(item.book.publisher)[0]
                                                         + float(item.count * item.price))})
            else:
                publishers.update({item.book.publisher: (item.count, float(item.count * item.price))})

        return render(request, "pub_sales.html", {"report": report,
                                                   "publishers": publishers})
    else:
        raise PermissionDenied


def eod_view(request):
    if request.user.is_authenticated and request.user.member.is_client:
        reports = EodReport.objects.all().order_by('date')
        return render(request, "eod_view.html", {"reports": reports})
    else:
        raise PermissionDenied


def book_sales_view(request):
    if request.user.is_authenticated and request.user.member.is_client:
        reports = BookSalesReport.objects.all().order_by('date')
        return render(request, "book_sales_view.html", {"reports": reports})
    else:
        raise PermissionDenied


def publisher_sales_view(request):
    if request.user.is_authenticated and request.user.member.is_client:
        reports = PublisherSalesReport.objects.all()
        return render(request, "pub_sales_view.html", {"reports": reports})
    else:
        raise PermissionDenied


def reports_overview(request):
    if request.user.is_authenticated and request.user.member.is_client:
        return render(request, "reports_overview.html", {})
    else:
        raise PermissionDenied
