from django.urls import re_path

from cart import views as cart_views

app_name = "cart"

urlpatterns = [
    re_path(r'^checkout/$', cart_views.checkout, name='checkout'),
    re_path(r'^remove/(?P<slug>[\w-]+)/$', cart_views.remove, name='remove'),
    re_path(r'^$', cart_views.cart, name='cart')
]
