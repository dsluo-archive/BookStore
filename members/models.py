from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from binascii import hexlify

from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

from books.models import Book, Reservation
from vendors.models import Vendor

# Create your models here.


class Address(models.Model):
    location = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.address


def upload_location(instance, filename):
    return "%s/%s" % (instance.slug, filename)


class UserCreation(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreation, self).__init__(*args, **kwargs)

        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)

    primary_address = models.CharField(max_length=60)
    profile_picture = models.ImageField(upload_to=upload_location, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    birth_date = models.DateField(default=timezone.now)

    authentication_key = models.CharField(max_length=8, blank=True)

    # Of type Cart
    cart = models.OneToOneField('cart.Cart', related_name='cart', on_delete=models.CASCADE, null=True, blank=True)

    # Of type Book
    purchased = models.ManyToManyField(Book, blank=True)

    # Of type Reservation
    reserved = models.ManyToManyField(Reservation, blank=True)

    # Of type Order
    order = models.ManyToManyField('cart.Order', related_name='order', blank=True)

    # Of type Address
    saved_addresses = models.ManyToManyField(Address, related_name='address', blank=True)

    def get_absolute_url(self):
        return reverse("members:account", kwargs={"slug": self.slug})

    def __str__(self):
        return self.user.username


def create_slug(instance):
    current_id = User.objects.all().order_by("-id").first()
    if current_id:
        current_id = current_id.id
    else:
        current_id = 1

    return slugify(instance.user.username) + "-" + str(current_id)


def pre_save_member_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_member_receiver, sender=Member)
