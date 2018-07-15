from django.db import models
from django.utils import timezone

from books.models import Book
from cart.tasks import cancel_reservation


# Create your models here.


class CartItem(models.Model):
    reservation = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)
    book = models.ForeignKey(Book, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.name


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

            if reservation:
                cancel_reservation.apply_async(args=[member.slug, book.slug], countdown=432000)

            self.items.add(new_item)

    @staticmethod
    def cancel_purchase(member, book):
        cart_item = member.cart.items.all().filter(book=book)

        if cart_item:
            cart_item.delete()

    def __str__(self):
        return self.member.user.username


class Order(models.Model):
    cart = models.OneToOneField(Cart, null=True, on_delete=models.PROTECT)
    confirmation_number = models.IntegerField(blank=False)
    date = models.DateField(default=timezone.now, blank=False)
    address_used = models.OneToOneField("members.Address",
                                        related_name="address_used",
                                        null=True,
                                        on_delete=models.PROTECT)
