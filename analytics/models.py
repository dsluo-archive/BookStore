from django.db import models
from django.urls import reverse
from django.utils import timezone

from books.models import Book
from cart.models import Order, CartItem


def update_end_of_day_report(order, cancel_order):
    if cancel_order:
        current_report, created = EodReport.objects.get_or_create(date=order.date)
    else:
        current_report, created = EodReport.objects.get_or_create(date=timezone.now())

    # if created:
    #     current_report.date = timezone.now()
    #     current_report.save()

    if cancel_order:
        current_report.orders.remove(order)
    else:
        current_report.orders.add(order)


def update_low_inventory(low_book, check_all=False):
    report, created = LowInvReport.objects.get_or_create(id=1)

    if check_all:
        for book in report.low_inventory_books.all():
            if book.count_in_stock >= 10:
                report.low_inventory_books.remove(book)

    if low_book.count_in_stock < 10:
        report.low_inventory_books.add(low_book)


def update_book_and_publisher_sales(order, cancel_order):
    if cancel_order:
        current_book_report, book_report_created = BookSalesReport.objects.get_or_create(date=order.date)
        current_publisher_report, publisher_report_created = PublisherSalesReport.objects.get_or_create(
            date=order.date)
    else:
        current_book_report, book_report_created = BookSalesReport.objects.get_or_create(date=timezone.now())
        current_publisher_report, publisher_report_created = PublisherSalesReport.objects.get_or_create(
            date=timezone.now())

    # if book_report_created:
    #     current_book_report.date = timezone.now()
    #     current_book_report.save()
    # if publisher_report_created:
    #     current_publisher_report.date = timezone.now()
    #     current_publisher_report.save()

    for item in order.items.all():
        if cancel_order:
            current_book_report.book.remove(item)
            current_publisher_report.publisher.remove(item)
        else:
            current_book_report.book.add(item)
            current_publisher_report.publisher.add(item)


def update_reports(order, check_all=False, cancel_order=False):
    update_end_of_day_report(order, cancel_order)

    for item in order.items.all():
        update_low_inventory(item.book, check_all)

    update_book_and_publisher_sales(order, cancel_order)


class EodReport(models.Model):
    date = models.DateField(default=timezone.now, blank=False)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return str(self.date)

    def get_absolute_url(self):
        return reverse("analytics:eod_report", kwargs={"date": str(self.date)})


class LowInvReport(models.Model):
    low_inventory_books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return "Low Inventory Books"


class BookSalesReport(models.Model):
    date = models.DateField(default=timezone.now, blank=False)
    book = models.ManyToManyField(CartItem, blank=True)

    def __str__(self):
        return str(self.date)

    def get_absolute_url(self):
        return reverse("analytics:book_sales_report", kwargs={"date": str(self.date)})


class PublisherSalesReport(models.Model):
    date = models.DateField(default=timezone.now, blank=False)
    publisher = models.ManyToManyField(CartItem, blank=True)

    def __str__(self):
        return str(self.date)

    def get_absolute_url(self):
        return reverse("analytics:publisher_sales_report", kwargs={"date": str(self.date)})
