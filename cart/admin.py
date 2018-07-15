from django.contrib import admin

from cart.models import Cart, CartItem, Order


# Register your models here.
class CartItemModelAdmin(admin.ModelAdmin):
    list_display = ["book"]

    class Meta:
        model = CartItem


class CartModelAdmin(admin.ModelAdmin):
    list_display = ["member", "total"]

    def member(self, obj):
        return obj

    class Meta:
        model = Cart


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ["cart", "confirmation_number", "date"]
    search_fields = ["confirmation_number"]

    class Meta:
        model = Order


admin.site.register(Cart, CartModelAdmin)
admin.site.register(Order, OrderModelAdmin)
admin.site.register(CartItem, CartItemModelAdmin)
