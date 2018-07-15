from django import template

register = template.Library()


@register.filter(name='paginate')
def paginate(list, per_page):
    return [list[i:i + per_page] for i in range(0, len(list), per_page)]
