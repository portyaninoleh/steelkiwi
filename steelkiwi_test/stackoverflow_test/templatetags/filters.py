from datetime import datetime

from django import template

register = template.Library()


@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter(name='format_question_body')
def format_question_body(value, arg):
    arg = int(arg)
    if len(value) > arg:
        value = value[:arg]
    return value


@register.filter(name='time_formatter')
def time_formatter(value, arg):
    return datetime.strftime(value, arg)