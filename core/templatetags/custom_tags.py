from django import template

from django.utils.safestring import mark_safe
from django.contrib.humanize.templatetags.humanize import intcomma


register = template.Library()


@register.filter
def currency(value):
    value = intcomma(value)
    value = mark_safe(f'&euro; {value}')

    return value


@register.filter
def midway(list_of_objects):
    return int(len(list_of_objects) / 2)
