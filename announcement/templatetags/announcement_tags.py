from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def rounded_timesince(value, delimiter=None):
    """
    .
    """
    if value.split()[0] in ['1', '0'] and value.split()[1] in ['minutes', 'minute']:
        return 'just now' 
    return f"{value.split(delimiter)[0]} ago"