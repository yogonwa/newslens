from datetime import datetime
import pytz

EASTERN = pytz.timezone("US/Eastern")
UTC = pytz.utc

def et_to_utc(dt: datetime) -> datetime:
    """
    Convert a naive or aware datetime in US/Eastern to UTC (returns aware UTC datetime).
    """
    assert isinstance(dt, datetime), "Input must be a datetime object"
    if dt.tzinfo is None:
        dt = EASTERN.localize(dt)
    else:
        dt = dt.astimezone(EASTERN)
    return dt.astimezone(UTC)

def utc_to_et(dt: datetime) -> datetime:
    """
    Convert a naive or aware UTC datetime to US/Eastern (returns aware ET datetime).
    """
    assert isinstance(dt, datetime), "Input must be a datetime object"
    if dt.tzinfo is None:
        dt = UTC.localize(dt)
    else:
        dt = dt.astimezone(UTC)
    return dt.astimezone(EASTERN) 