from django import template

register = template.Library()


@register.simple_tag()
def total_price(items, *args, **kwargs):
    total = 0
    for item in items:
        total += (item.price * item.count)

    return total
