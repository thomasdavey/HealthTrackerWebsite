from django import template

register = template.Library()


@register.filter(name='add')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})
