from django.db import models
from django.utils import timezone

from books.models import Book, Publisher
# Create your models here.
from cart.models import Order


class EodReport(models.Model):
    date = models.DateField(default=timezone.now, blank=False)
    orders = models.ManyToManyField(Order)


class LowInvReport(models.Model):
    date = models.DateField(default=timezone.now, blank=False)
    low_inventory_books = models.ManyToManyField(Book, blank=True)


class BookSalesReport(models.Model):
    date = models.DateField(default=timezone.now, blank=False)
    book = models.OneToOneField(Book, on_delete=models.PROTECT, blank=True)


class PublisherSalesReport(models.Model):
    date = models.DateField(default=timezone.now, blank=False)
    publisher = models.OneToOneField(Publisher, on_delete=models.PROTECT, blank=True)
