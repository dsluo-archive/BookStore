from django.core.exceptions import PermissionDenied
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from books.models import Book, PromotionCodes
from cart.models import Order, UserCheckout, order_id_generator
from cart.tasks import cancel_reservation

# Create your views here.


reservation_cancellation_timer = 432000  # (5 days)


def cart(request):

    if request.user.is_authenticated:
        code = request.POST.get("promo_code")

        if code:
            promotion = PromotionCodes.objects.all().filter(code=code).first()

            if promotion:
                for cart_item in request.user.member.cart.items.all():
                    for genre in promotion.genres.all():
                        if genre.book_set.all().filter(slug=cart_item.book.slug):
                            cart_item.price = float(cart_item.book.price) * (1-float(promotion.discount))
                            cart_item.save()
                            break
                        else:
                            cart_item.price = cart_item.book.price
                            cart_item.save()
            else:
                for cart_item in request.user.member.cart.items.all():
                    cart_item.price = cart_item.book.price
                    cart_item.save()
        else:
            code = ""

        return render(request, "cart.html", {"items": request.user.member.cart.items.all(),
                                             "current_code": code})
    else:
        return HttpResponseRedirect(reverse('members:login'))


def remove(request, slug):
    book = Book.objects.all().filter(slug=slug).first()
    request.user.member.cart.remove_item(request.user.member, book)

    return HttpResponseRedirect(reverse('cart:cart'))


def checkout(request):
    if request.user.is_authenticated:
        if not request.user.member.cart.items.exists():
            return HttpResponseRedirect(reverse('cart:cart'))
        else:
            purchase = request.POST.get("card")
            reserve = request.POST.get("cash")

            if purchase:
                user_checkout, created = UserCheckout.objects.get_or_create(user=request.user, reservation=False)
                client_token = user_checkout.get_client_token()
                return render(request, "checkout.html", {"cart": request.user.member.cart.items.all(),
                                                         "client_token": client_token})
            elif reserve:
                user_cart = request.user.member.cart.items.all()
                order_id = order_id_generator()

                while Order.objects.all().filter(confirmation_number=order_id).exists():
                    order_id = order_id_generator()

                new_order = Order(confirmation_number=order_id,
                                  address_used=request.user.member.primary_address,
                                  reservation=True)
                new_order.save()

                for item in user_cart:
                    new_order.items.add(item)

                request.user.member.orders.add(new_order)
                new_order.save()

                cancel_reservation.apply_async(args=[new_order.confirmation_number],
                                               countdown=reservation_cancellation_timer)  # 5 days

                for item in request.user.member.cart.items.all():
                    request.user.member.cart.remove_item(request.user.member, item.book)

                return HttpResponseRedirect(reverse("cart:summary", kwargs={"order": new_order.confirmation_number}))
            else:
                raise PermissionDenied
    else:
        raise PermissionDenied


def submit(request):
    if request.user.is_authenticated:
        if not request.user.member.cart.items.exists():
            return HttpResponseRedirect(reverse('cart:cart'))
        else:
            user_cart = request.user.member.cart.items.all()

            order_id = order_id_generator()

            while Order.objects.all().filter(confirmation_number=order_id).exists():
                order_id = order_id_generator()

            new_order = Order(confirmation_number=order_id,
                              address_used=request.user.member.primary_address,
                              reservation=False)
            new_order.save()

            for item in user_cart:
                new_order.items.add(item)

            request.user.member.orders.add(new_order)
            new_order.save()

            for item in request.user.member.cart.items.all():
                request.user.member.cart.remove_item(request.user.member, item.book)

            return HttpResponseRedirect(reverse("cart:summary", kwargs={"order": new_order.confirmation_number}))
    else:
        raise PermissionDenied


def order_detail(request, order):
    if request.user.is_authenticated:
        order = request.user.member.orders.all().filter(confirmation_number=order).first()
        if order:
            items = order.items.all()
            return render(request, "order_detail.html", {"order": order,
                                                         "items": items,
                                                         "reservation": order.reservation})
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied

