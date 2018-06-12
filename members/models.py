from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from binascii import hexlify

from django.contrib.auth.models import User
from books.models import Reservation
from vendors.models import Vendor
from client.models import Client


# Create your models here.


class Address(models.Model):
    address = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.address


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Username, Email, First/Last name, Password
    profile_picture = models.ImageField(upload_to=upload_location, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    birth_date = models.DateField()
    recv_newsletter = models.BooleanField(default=True)
    account_active = models.BooleanField(default=True)  # set to False if account is deleted, disallows login

    authenticated = models.BooleanField(default=False)  # user responded to emailed key
    authentication_key = models.CharField(max_length=8, blank=True)

    admin = models.BooleanField(default=False)

    id = models.AutoField(primary_key=True)

    # If member is a vendor
    vendor_auth = models.BooleanField(default=False)
    vendor_actual = models.OneToOneField(Vendor, on_delete=models.CASCADE, null=True, blank=True)

    # If member is a client
    client_auth = models.BooleanField(default=False)
    client_actual = models.OneToOneField(Client, on_delete=models.CASCADE, null=True, blank=True)

    # Of type Cart
    cart = models.OneToOneField('cart.Cart', related_name='+', on_delete=models.CASCADE, null=True, blank=True)

    # Of type Book
    purchased = models.ManyToManyField('books.Book', related_name='+', blank=True)

    # Of type Reservation
    reserved = models.ManyToManyField(Reservation, blank=True)

    # Of type Order
    order = models.ManyToManyField('cart.Order', related_name='+', blank=True)

    # Of type Address
    saved_addresses = models.ManyToManyField(Address, related_name='+', blank=True)

    def get_absolute_url(self):
        return reverse("members:account", kwargs={"slug": self.slug})

    def __str__(self):
        return self.user.first_name + self.user.last_name


def create_slug(instance):
    current_id = Member.objects.all().order_by("-id").first()
    if current_id:
        current_id = current_id.id
    else:
        current_id = 1

    return slugify(instance.user.first_name) + "-" + slugify(instance.user.last_name) + "-" + str(current_id)


def pre_save_member_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_member_receiver, sender=Member)
