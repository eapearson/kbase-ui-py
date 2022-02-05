from django import template
from datetime import datetime, timezone
from dateutil import tz
from dateutil.parser import parse
from dateutil.utils import default_tzinfo

register = template.Library()

UTC = tz.gettz("UTC")


def utc_from_string(value):
    return default_tzinfo(parse(value), UTC)


def utc_from_epoch_ms(value):
    return datetime.fromtimestamp(value / 1000.0, timezone.utc)
