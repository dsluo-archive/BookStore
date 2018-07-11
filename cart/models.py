from django.db import models
from django.utils import timezone

# Create your models here.

from books.models import Book


class CartItem(models.Model):
    reservation = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)
    book = models.ForeignKey(Book, null=False, blank=False, on_delete=models.CASCADE)


class Cart(models.Model):
    items = models.ManyToManyField(CartItem,
                                  blank=True)

    total = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                default=0.00,
                                blank=True)

    def add_purchase(self, member, book, count, reservation):

        cart_item = member.cart.items.all().filter(book=book).first()

        if cart_item:
            cart_item.count = count
            cart_item.save()
        else:
            new_item = CartItem(reservation=reservation, count=count, book=book)
            new_item.save()

            self.items.add(new_item)

    def cancel_purchase(self, member, book):
        cart_item = member.cart.items.all().filter(book=book)

        if cart_item:
            cart_item.delete()


class Order(models.Model):
    cart = models.OneToOneField(Cart, null=True, on_delete=models.PROTECT)
    confirmation_number = models.IntegerField(blank=False)
    date = models.DateField(default=timezone.now, blank=False)
    address_used = models.OneToOneField("members.Address",
                                        related_name="address_used",
                                        null=True,
                                        on_delete=models.PROTECT)
