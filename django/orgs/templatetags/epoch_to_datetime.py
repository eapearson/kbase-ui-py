from django import template
import datetime

register = template.Library()

@register.filter
def epoch_to_datetime(value):
    d = datetime.datetime.fromtimestamp(value/1000)
    return d
