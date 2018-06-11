from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.utils import timezone

# Create your models here.

from books.models import Book
from members.models import Address


class Cart(models.Model):

    member_owner = models.OneToOneField('members.Member', on_delete=models.PROTECT, related_name='+')
    books = models.ManyToManyField(Book, blank=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=True)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.PROTECT)
    confirmation_number = models.IntegerField(blank=False)
    date = models.DateField(default=timezone.now, blank=False)
    address_used = models.OneToOneField(Address, on_delete=models.PROTECT)

