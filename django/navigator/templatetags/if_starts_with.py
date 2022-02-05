from django import template

register = template.Library()


@register.simple_tag
def if_starts_with(compare1, compare2, result):
    if compare1.startswith(compare2):
        return result
    else:
        return ""


# @register.filter()
# def starts_with(value, arg):
#     if isinstance(value, str):
#         return value.startswith(arg)
#     return False
