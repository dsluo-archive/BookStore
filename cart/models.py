from django.db import models
from django.utils import timezone

# Create your models here.

from books.models import Book


class Cart(models.Model):
    books = models.ManyToManyField(Book,
                                   blank=True)

    total = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                default=0.00,
                                blank=True)

    def add_purchase(self, book, count):
        pass

    def add_reservation(self, book, count):
        pass


class Order(models.Model):
    cart = models.OneToOneField(Cart, null=True, on_delete=models.PROTECT)
    confirmation_number = models.IntegerField(blank=False)
    date = models.DateField(default=timezone.now, blank=False)
    address_used = models.OneToOneField("members.Address", related_name="address_used", null=True, on_delete=models.PROTECT)
