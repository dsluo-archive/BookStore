import random
import string

import braintree
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils import timezone

from books.models import Book

if settings.DEBUG:
    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            environment=braintree.Environment.Sandbox,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC,
            private_key=settings.BRAINTREE_PRIVATE
        )
    )


# Create your models here.


class CartItem(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)
    book = models.ForeignKey(Book, null=False, blank=False, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=False)

    def __str__(self):
        return self.book.name


class Cart(models.Model):
    items = models.ManyToManyField(CartItem,
                                   blank=True)

    total = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                default=0.00,
                                blank=True)

    def add_item(self, member, book, count):

        cart_item = member.cart.items.all().filter(book=book).first()

        if int(count) > book.count_in_stock:
            return False
        else:
            if cart_item:
                cart_item.count = count
                cart_item.save()
            else:
                new_item = CartItem(count=count, book=book, price=book.price)
                new_item.save()

                self.items.add(new_item)

            return True

    @staticmethod
    def remove_item(member, book):
        cart_item = member.cart.items.all().filter(book=book).first()

        if cart_item:
            member.cart.items.remove(cart_item)

    def __str__(self):
        return self.member.user.username


class UserCheckout(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    braintree_id = models.CharField(max_length=120, null=True, blank=True)
    reservation = models.BooleanField(default=False)

    def __str__(self):
        return self.user

    @property
    def get_braintree_id(self):
        if not self.braintree_id:
            result = gateway.customer.create({
                "email": "jen@example.com",
            })

            if result.is_success:
                self.braintree_id = result.customer.id
                self.save()

        return self.braintree_id

    def get_client_token(self):
        customer_id = self.get_braintree_id

        if customer_id:
            client_token = gateway.client_token.generate({
                "customer_id": customer_id
            })

            return client_token
        else:
            return None


def update_braintree_id(sender, instance, *args, **kwargs):
    if not instance.braintree_id:
        return instance.get_braintree_id


class Order(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)
    confirmation_number = models.CharField(max_length=10, unique=True, blank=False)
    date = models.DateField(default=timezone.now, blank=False)
    address_used = models.ForeignKey("members.Address",
                                     related_name="address_used",
                                     null=True,
                                     on_delete=models.SET_NULL)
    reservation = models.BooleanField(default=False)
    is_fulfilled = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("cart:summary", kwargs={"order": self.confirmation_number})

    @property
    def price(self):
        price = 0.0
        for item in self.items.all():
            price += float(item.price)

        return "%.2f" % price

    def cancel_order(self):
        from analytics.models import update_reports

        user = self.member_set.first().user
        all_items = ''

        for item in self.items.all():
            item.book.count_in_stock += item.count
            item.book.save()
            all_items += item.book.name + ', '

        update_reports(self, cancel_order=True)

        send_mail(
            'Your order has been cancelled',

            user.username + ',\n\nThe following order has been cancelled:' + '\n'
            + "Customer: " + user.first_name + ' ' + user.last_name + '\n'
            + "Order Confirmation Number: " + self.confirmation_number + '\n'
            + 'Order ID: ' + str(self.id) + '\n'
            + 'Date Order was Placed: ' + str(self.date)[0:10] + '\n'
            + 'Address Used: ' + self.address_used.location + '\n'
            + 'Items ordered: ' + all_items[:-2] + '\n'
            + 'Total amount: ' + self.price + '\n\n'
            + 'If this is an error, please contact support at thedogearbookstore@gmail.com',

            'thedogearbookstore@gmail.com',
            [user.email],
            fail_silently=True,
        )

        for item in self.items.all():
            item.delete()
        self.delete()

    def __str__(self):
        return self.confirmation_number


def order_id_generator():
    order_id = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
    return order_id


def post_save_order_receiver(sender, instance, created, **kwargs):
    if instance.items.all().first():
        user = instance.member_set.first().user
        all_items = ''

        for item in instance.items.all():
            all_items += item.book.name + ', '

        send_mail(
            'Your order has been placed',

            user.username + ',\n\nThe following order has been placed:' + '\n\n'
            + "Customer: " + user.first_name + ' ' + user.last_name + '\n'
            + "Order Confirmation Number: " + instance.confirmation_number + '\n'
            + 'Order ID: ' + str(instance.id) + '\n'
            + 'Date Order was Placed: ' + str(instance.date)[0:10] + '\n'
            + 'Address Used: ' + instance.address_used.location + '\n'
            + 'Items ordered: ' + all_items[:-2] + '\n'
            + 'Total amount: ' + instance.price + '\n\n'
            + 'If this is an error, please contact support at thedogearbookstore@gmail.com',

            'thedogearbookstore@gmail.com',
            [user.email],
            fail_silently=True,
        )


post_save.connect(update_braintree_id, sender=UserCheckout)
post_save.connect(post_save_order_receiver, sender=Order)
