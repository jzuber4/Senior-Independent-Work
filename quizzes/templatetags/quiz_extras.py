from django import template

register = template.Library()

# http://stackoverflow.com/questions/9948095/variable-subtraction-in-django-templates
@register.filter
def subtract(value, arg):
    return value - arg
