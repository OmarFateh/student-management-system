from django import template

register = template.Library()

@register.simple_tag
def is_in(var, *obj):
    """
    Take variable and list of objects, and check if the variable is in the list.
    """
    return var in obj