from django import template
from datetime import datetime, timezone
import math
from lib import utils

register = template.Library()


@register.filter()
def nice_elapsed_time(value):
    now = datetime.now(timezone.utc)
    try:
        if isinstance(value, str):
            date = utils.utc_from_string(value)
        elif isinstance(value, int):
            date = utils.utc_from_epoch_ms(value)
        else:
            date = value

        time_elapsed = now - date

        if time_elapsed.days <= 30:
            if time_elapsed.days == 0:
                hours = time_elapsed.seconds / 3600
                if hours < 1:
                    minutes = time_elapsed.seconds / 60
                    if minutes < 1:
                        return f"{time_elapsed.seconds} seconds ago"
                    else:
                        return f"{math.floor(hours)} minutes ago"
                else:
                    return f"{math.floor(hours)} hours ago"
            else:
                return f"{time_elapsed.days} days ago"
        elif date.year == now.year:
            return date.strftime("%b %-d")
            # return date.strftime("%m/%d")
        else:
            # return date.strftime("%b %-d, %Y")
            return date.strftime("%Y-%-m-%-d")
    except ValueError as ve:
        return f"Error: {str(ve)}"
    except Exception as ex:
        return f"Error: {str(ex)}"
