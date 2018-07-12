from django import template

register = template.Library()


@register.simple_tag()
def unit_price(count, price, *args, **kwargs):
    return count * price

