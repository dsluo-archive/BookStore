from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save


# Create your models here.


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class Client(models.Model):
    member_actual = models.OneToOneField('members.Member', related_name='+', on_delete=models.CASCADE)

    end_of_day_report = models.ManyToManyField('analytics.EodReport', related_name='+', blank=True)
    low_inventory_report = models.ManyToManyField('analytics.LowInvReport', related_name='+', blank=True)
    book_sales_report = models.ManyToManyField('analytics.BookSalesReport', related_name='+', blank=True)

    # publisher_sales_report = models.ManyToManyField(PublisherSalesReport, related_name='+', blank=True)

    def __str__(self):
        return self.member_actual.user.first_name + self.member_actual.user.last_name
