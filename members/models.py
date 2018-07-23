import random
import string

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils.text import slugify

from books.models import Book
from cart.models import Cart, Order
from vendors.models import Vendor


# Create your models here.


class Address(models.Model):
    location = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.location


def upload_location(instance, filename):
    return "%s/%s/%s" % ("members", instance.slug, filename)


class UserCreation(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreation, self).__init__(*args, **kwargs)

        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    is_client = models.BooleanField(default=False)

    primary_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=False)
    profile_picture = models.ImageField(upload_to=upload_location,
                                        default="members/images/default_member.jpg",
                                        null=False,
                                        blank=False)
    slug = models.SlugField(unique=True, blank=True)
    birth_date = models.DateField(blank=False)
    receive_newsletter = models.BooleanField(default=True, null=False)
    hex_code = models.CharField(max_length=10, blank=True, null=True)
    activated = models.BooleanField(default=False, blank=False)

    authentication_key = models.CharField(max_length=8, blank=True)

    # Of type Cart
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, null=True, blank=True)

    # Of type Book
    purchased = models.ManyToManyField(Book, blank=True)

    # Of type Order
    orders = models.ManyToManyField(Order, blank=True)

    # Of type Address
    saved_addresses = models.ManyToManyField(Address, related_name='address', blank=True)

    def get_absolute_url(self):
        return reverse("members:account", kwargs={"slug": self.slug})

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        self.cart.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


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
    
    if instance.id:
        instance.saved_addresses.add(instance.primary_address)


def post_save_member_receiver(sender, instance, created, **kwargs):
    if created:
        new_cart = Cart.objects.create()
        instance.cart = new_cart
        instance.save()

        instance.hex_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        instance.save()

        send_mail(
            'Welcome to The Dog Ear Bookstore',

            'Welcome!\n\nPlease confirm your account using the following code:'
            + instance.hex_code
            + '\n\nhttp://localhost:8000/account/activate/'
            + instance.slug,

            'thedogearbookstore@example.com',
            [instance.user.email],
            fail_silently=True,
        )

pre_save.connect(pre_save_member_receiver, sender=Member)
post_save.connect(post_save_member_receiver, sender=Member)
