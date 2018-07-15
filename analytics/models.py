from django.db import models
from django.utils import timezone

from books.models import Book
# Create your models here.
from cart.models import Order


class EodReport(models.Model):
    date = models.DateField(default=timezone.now)
    orders = models.ManyToManyField(Order)


class LowInvReport(models.Model):
    date = models.DateField(default=timezone.now)
    low_inventory_books = models.ManyToManyField(Book, blank=True)


class BookSalesReport(models.Model):
    date = models.DateField(default=timezone.now)
    book = models.OneToOneField(Book, on_delete=models.PROTECT, blank=True)


class PublisherSalesReport(models.Model):
    pass
