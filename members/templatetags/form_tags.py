from django import template
from django.forms import fields

register = template.Library()


@register.filter(name='is_field')
def is_field(field, type):
    try:
        klass = getattr(fields, type)
        return field.field.widget.__class__.__name__ == klass.__name__
    except AttributeError:
        return False
