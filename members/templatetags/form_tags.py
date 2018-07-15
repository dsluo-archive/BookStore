from django import template
from django.forms import CheckboxInput, FileField

register = template.Library()


@register.filter(name='is_checkbox')
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__


@register.filter(name='is_file_upload')
def is_file_upload(field):
    return field.field.widget.__class__.__name__ == FileField().__class__.__name__
