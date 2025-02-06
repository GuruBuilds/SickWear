from django import template

register = template.Library()

@register.filter
def getattr(obj, attr):
    """Retrieve an attribute from an object in templates."""
    return getattr(obj, attr, None)
