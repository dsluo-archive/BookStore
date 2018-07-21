from django import template

register = template.Library()


@register.simple_tag()
def book_report_total(report, *args, **kwargs):
    total = 0
    for item in report.book.all():
        total += (item.price * item.count)

    return total
