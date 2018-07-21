from django.shortcuts import render

from analytics.models import EodReport, LowInvReport, BookSalesReport, PublisherSalesReport
# Create your views here.


def eod_report(request, date):
    report = EodReport.objects.all().filter(date=date).first()
    return render(request, "eod_report.html", {"report": report})


def low_inv_report(request):
    report = LowInvReport.objects.first()
    return render(request, "inventory.html", {"report": report})


def book_sales_report(request, date):
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


def publisher_sales_report(request, date):
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


def eod_view(request):
    reports = EodReport.objects.all().order_by('date')
    return render(request, "eod_view.html", {"reports": reports})


def book_sales_view(request):
    reports = BookSalesReport.objects.all().order_by('date')
    return render(request, "book_sales_view.html", {"reports": reports})


def publisher_sales_view(request):
    reports = PublisherSalesReport.objects.all()
    return render(request, "pub_sales_view.html", {"reports": reports})


def reports_overview(request):
    return render(request, "reports_overview.html", {})
