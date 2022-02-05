from django import template
import datetime

register = template.Library()


@register.filter()
def nice_date(value):
    now = datetime.datetime.utcnow()
    try:
        if isinstance(value, str):
            date = datetime.datetime.strptime(value, "%Y-%m-%d")
        elif isinstance(value, int):
            date = datetime.datetime.utcfromtimestamp(value / 1000)
        else:
            date = value
        if date.year == now.year:
            return date.strftime("%b %-d")
            # return date.strftime("%m/%d")
        else:
            return date.strftime("%b %-d, %Y")
            # return date.strftime("%m/%d/%Y")
    except ValueError as ve:
        return f"Error: {str(ve)}"
    except Exception as ex:
        return f"Error: {str(ex)}"
