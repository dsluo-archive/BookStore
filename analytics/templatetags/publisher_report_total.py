from django import template

register = template.Library()


@register.simple_tag()
def publisher_report_total(report, *args, **kwargs):
    total = 0
    for item in report.publisher.all():
        total += (item.price * item.count)

    return total
