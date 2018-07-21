from django import template

register = template.Library()


@register.simple_tag()
def eod_total(report, *args, **kwargs):
    total = 0
    for order in report.orders.all():
        for item in order.items.all():
            total += (item.price * item.count)

    return total
