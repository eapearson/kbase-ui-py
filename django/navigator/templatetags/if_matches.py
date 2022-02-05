from django import template
import re

register = template.Library()


@register.simple_tag
def if_matches(compare1, compare2, result):
    if re.match(compare1, compare2):
        return result
    else:
        return ""
