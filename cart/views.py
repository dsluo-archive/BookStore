import braintree
from random import shuffle

from django.contrib import messages
from django.contrib.auth import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.urls import reverse

from members.models import Address
from books.models import Book, PromotionCodes
from cart.models import Order, UserCheckout, order_id_generator
from cart.tasks import cancel_reservation
from analytics.models import update_reports

# Create your views here.


reservation_cancellation_timer = 432000  # (5 days)

if settings.DEBUG:
    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            environment=braintree.Environment.Sandbox,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC,
            private_key=settings.BRAINTREE_PRIVATE
        )
    )


def cart(request):
    if request.user.is_authenticated:
        code = request.POST.get("promo_code")

        if code:
            promotion = PromotionCodes.objects.all().filter(code=code).first()

            if promotion:
                for cart_item in request.user.member.cart.items.all():
                    for genre in promotion.genres.all():
                        if genre.book_set.all().filter(slug=cart_item.book.slug):
                            cart_item.price = float(cart_item.book.price) * (1 - float(promotion.discount))
                            cart_item.save()
                            break
                        else:
                            cart_item.price = cart_item.book.price
                            cart_item.save()

                messages.success(request, "Promotional " + code + " applied!")
            else:
                for cart_item in request.user.member.cart.items.all():
                    cart_item.price = cart_item.book.price
                    cart_item.save()

                messages.warning(request, "Promotional " + code + " could not be found!")

        else:
            code = ""

        genres = []
        for item in request.user.member.cart.items.all():
            genres.extend(item.book.subjects.all())
        genres = list(set(genres))
        shuffle(genres)

        books = []
        for genre in genres:
            books.extend(genre.book_set.all())
        books = list(set(books))[:5]

        return render(request, "cart.html", {"items":         request.user.member.cart.items.all(),
                                             "current_code":  code,
                                             "similar_items": books})
    else:
        return HttpResponseRedirect(reverse('members:login'))


def remove(request, slug):
    book = Book.objects.all().filter(slug=slug).first()
    request.user.member.cart.remove_item(request.user.member, book)

    return HttpResponseRedirect(reverse('cart:cart'))


def check_stock(request, cart_items):
    cart_messages = []
    for item in cart_items:
        if item.count > item.book.count_in_stock:
            if item.book.count_in_stock == 0:
                request.user.member.cart.remove_item(request.user.member, item.book)
                custom_message = " The item is out of stock and has been removed from your cart. We " \
                                 "apologize for the inconvenience."
            else:
                item.count = item.book.count_in_stock
                item.save()
                custom_message = "Stock for current item is fewer than in cart. Item count set to " \
                                 + str(item.book.count_in_stock) + "."
            cart_messages.append(messages.warning(request, item.book.name + ": " + custom_message))

    return cart_messages


def checkout(request):
    if request.user.is_authenticated:
        if not request.user.member.cart.items.exists():
            return HttpResponseRedirect(reverse('cart:cart'))
        else:
            purchase = request.POST.get("card")
            reserve = request.POST.get("cash")

            cart_items = request.user.member.cart.items.all()

            if purchase:
                user_checkout, created = UserCheckout.objects.get_or_create(user=request.user, reservation=False)
                client_token = user_checkout.get_client_token()
                return render(request, "checkout.html", {"cart":         cart_items,
                                                         "client_token": client_token})
            elif reserve:

                cart_messages = check_stock(request, cart_items)

                if cart_messages:
                    return HttpResponseRedirect(reverse('cart:cart'))

                for item in cart_items:
                    item.book.count_in_stock -= item.count
                    item.book.save()

                order_id = order_id_generator()

                while Order.objects.all().filter(confirmation_number=order_id).exists():
                    order_id = order_id_generator()

                new_order = Order(confirmation_number=order_id,
                                  address_used=request.user.member.primary_address,
                                  reservation=True)
                new_order.save()

                for item in cart_items:
                    new_order.items.add(item)

                request.user.member.orders.add(new_order)
                new_order.save()

                update_reports(new_order)

                cancel_reservation.apply_async(args=[new_order.confirmation_number],
                                               countdown=reservation_cancellation_timer)  # 5 days

                for item in request.user.member.cart.items.all():
                    request.user.member.cart.remove_item(request.user.member, item.book)

                return HttpResponseRedirect(reverse("cart:summary", kwargs={"order": new_order.confirmation_number}))
            else:
                return HttpResponseRedirect(reverse('cart:cart'))
    else:
        raise PermissionDenied


def submit(request):
    if request.user.is_authenticated:
        if not request.user.member.cart.items.exists():
            return HttpResponseRedirect(reverse('cart:cart'))
        else:
            user_cart = request.user.member.cart.items.all()

            price = 0.0
            for item in user_cart:
                price += float(item.price) * item.count

            nonce = request.POST.get("payment_method_nonce")

            if nonce:
                cart_messages = check_stock(request, user_cart)

                if cart_messages:
                    return HttpResponseRedirect(reverse('cart:cart'))

                order_id = order_id_generator()

                while Order.objects.all().filter(confirmation_number=order_id).exists():
                    order_id = order_id_generator()

                result = gateway.transaction.sale({
                    "amount": str(price),
                    "payment_method_nonce": nonce,
                    "order_id": order_id,
                    "options": {
                        "submit_for_settlement": True
                    }
                })

                if result.is_success:

                    for item in user_cart:
                        item.book.count_in_stock -= item.count
                        item.book.save()

                    address = request.POST.get("new_address")
                    save_address = request.POST.get("save_address")

                    if address:
                        if save_address:
                            address, created = Address.objects.get_or_create(location=address)
                            request.user.member.saved_addresses.add(address)
                            request.user.member.save()
                    else:
                        for saved_address in request.user.member.saved_addresses.all():
                            if request.POST.get(saved_address.location):
                                address = saved_address

                    if not address:
                        address = request.user.member.primary_address

                    new_order = Order(confirmation_number=order_id,
                                      address_used=address,
                                      reservation=False,
                                      is_fulfilled=True)
                    new_order.save()

                    for item in user_cart:
                        new_order.items.add(item)

                    request.user.member.orders.add(new_order)
                    new_order.save()

                    update_reports(new_order)

                    for item in request.user.member.cart.items.all():
                        request.user.member.cart.remove_item(request.user.member, item.book)

                    return HttpResponseRedirect(reverse("cart:summary", kwargs={"order": new_order.confirmation_number}))
                else:
                    messages.warning(request, "Payment was declined. Please try again later.")
                    return HttpResponseRedirect(reverse('cart:checkout'))
            else:
                raise PermissionDenied
    else:
        raise PermissionDenied


def order_detail(request, order):
    if request.user.is_authenticated:
        order = request.user.member.orders.all().filter(confirmation_number=order).first()
        if order:
            items = order.items.all()
            return render(request, "order_detail.html", {"order":       order,
                                                         "items":       items,
                                                         "reservation": order.reservation})
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied


def order_cancel(request, order):
    current_order = get_object_or_404(Order, confirmation_number=order)
    confirmation = request.POST.get('confirmation')

    if confirmation == "Yes, I want to cancel my reservation.":
        current_order.cancel_order()

        messages.success(request, "Reservation successfully cancelled.")
        return HttpResponseRedirect(reverse('members:default_account'))
    else:
        if current_order.reservation:
            return render(request, "delete_order.html", {})
        else:
            raise PermissionDenied
