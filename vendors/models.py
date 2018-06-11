from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save

from books.models import Book

# Create your models here.


def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)


class Vendor(models.Model):

    vendor_name = models.CharField(max_length=60)
    member_actual = models.OneToOneField('members.Member', related_name='+', on_delete=models.CASCADE)
    books_owned = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.member_actual.user.first_name + self.member_actual.user.last_name
