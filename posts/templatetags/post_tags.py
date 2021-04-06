from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def rounded_timesince(value, delimiter=None):
    """
    Take value of time and delimiter.
    Split the value by the delimiter, and return the digit and the first letter of the time.
    eg: minutes = min, hour = h, week = w, year = y.
    """
    time_chunk = value.split(delimiter)[0].split()
    digit = time_chunk[0]
    letter = time_chunk[1][0]
    if time_chunk[1] in ["minute", "minutes"]:
        letter = 'min'    
    if value.split()[0] == "0" and value.split()[1][0] == "m":
        return 'just now'       
    return f'{digit} {letter}'
