""" Any spatial and temporal related functions.
"""

# Standard library
import datetime
import re
import sys
from typing import List

# 3rd Party Library
from astral import Observer, sun
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

def addressToLatLong(address: str):
    """ Find the latitude and longitude when given an address.

    Args:
        address (str): Address format: "city state country"

    Returns:
        dict: [lat: float, lon: float]
    """

    try:
        if not re.fullmatch("([a-zA-Z.\- ]+) ([a-zA-Z.\- ]+) ([a-zA-Z.\- ]+)", address):
            raise ValueError("No address provided or incorrect format address string: 'city state country'\n")
            sys.exit(-1)
        
        geo = Nominatim(user_agent="mind-your-own-beeswax")
        loc = geo.geocode(address)
        return [loc.latitude, loc.longitude]
        
    except ValueError as e:
        print(e)
        sys.exit(1)
    except AttributeError as e:
        print(f"Could not obtain location based on provided address: {address}")
        sys.exit(1)


def getSunPeriodTerms() -> List[str]:
    """ Terminology that references the sun's position during different periods of the day.

    Returns:
        List[str]: different periods in the day
    """

    options = (sun.sun(Observer(0, 0), date=datetime.date(1, 1, 1))).keys()
    return [ opt for opt in options ]


def getSolarTime(address: str=None, lat: float=32.943608, lon: float=35.091979, period: str='sunset', date: datetime=datetime.date.today()):
    """Calculates the time during the day when the sun is positioned at the specified period (e.g., noon).

    Args:
        lat (float): latitude
        lon (float): longitude
        address (str): city, state, and country if no latitude/longitude provided
        period (str, optional): The word that specifies a specific period of day. Defaults to 'sunset'.
        date (datetime, optional): The date to check. Defaults to datetime.date.today().

    Returns:
        datetime: time
    """
    if (lat == "" and lon == ""):
        lat, lon = addressToLatLong(address)
        # print(">> lat, lon >>", lat, lon)

    try:
        tz = TimezoneFinder().timezone_at(lat=float(lat), lng=float(lon))
    except TypeError:
        print("Unable to cast latitude and longitude as float.")

    s = sun.sun(Observer(lat, lon), date=date, tzinfo=tz)
    return s[period]


def datetimeToEpoch(value: datetime) -> int:
    """ Takes datetime and converts to epoch timestamp

    Args:
        value (datetime): date and time

    Returns:
        int: epoch timestamp
    """

    return int(value.timestamp() * 1e3)


def epochToDatetime(value: int):
    """ Converts epoch (in milliseconds) to human-readable date and time.

    Args:
        value (int): epoch timestamp or integer equivalent

    Returns:
        datetime: date and time
    """

    return datetime.datetime.fromtimestamp((value / 1000.0)).strftime('%Y-%m-%d %H:%M:%S.%f')

def timeRange(target) -> tuple:
    """Provides a range of 30 minutes before and after the provided target time.
    Will adjust the range if the end is set to a future time, and move the beginning of the range back by one hour.

    Args:
        target (datetime): desired time to calculate 

    Returns:
        tuple: A tuple with two integers representing epoch time in the position of (start, end)
    """
    start = target - datetime.timedelta(minutes=30)
    end = target + datetime.timedelta(minutes=30)

    # Prevent program from becoming psychic.
    if end.timestamp() > datetime.datetime.now().timestamp():
        start = target - datetime.timedelta(hours=1)
        end = datetime.datetime.now()
    
    return (datetimeToEpoch(start), datetimeToEpoch(end))
    

def nearestTime(target: (datetime, int), data: list):
    """ Finds the closest time to a target given a list

    Args:
        target (datetime, int): _description_
        data (list): _description_

    Returns:
        dict: _description_
    """

    if isinstance(target, datetime.datetime):
        target = datetimeToEpoch(target)

    return min(data, key=lambda x : abs(x.timestamp - target))
