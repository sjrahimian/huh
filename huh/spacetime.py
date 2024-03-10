""" Any spatial and temporal related functions.
"""

# Standard library
import datetime
import sys
from typing import List, Tuple, Union

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
        if not re.fullmatch("([a-zA-Z]+) ([a-zA-Z]+) ([a-zA-Z]+)", address):
            raise ValueError("Incorrect format address string: 'city state country'")
        
        geo = Nominatim(user_agent="mind-your-own-beeswax")
        loc = geo.geocode(address)
        return [loc.latitude, location.longitude]
        
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


def getSolarTime(lat: float, lon: float, period: str='sunset', date: datetime=datetime.date.today()) -> datetime:
    """Calculates the time during the day when the sun is positioned at the specified period (e.g., noon).

    Args:
        lat (float): _description_
        lon (float): _description_
        period (str, optional): The word that specifies a specific period of day. Defaults to 'sunset'.
        date (datetime, optional): The date to check. Defaults to datetime.date.today().

    Returns:
        datetime: time
    """

    tz = TimezoneFinder().timezone_at(lat=lat, lng=lon)
    s = sun.sun(Observer(lat, lon), date=date, tzinfo=tz)
    return s[optKey]


def convertToEpoch(from: datetime) -> int:
    """ Takes datetime and converts to epoch timestamp

    Args:
        from (datetime): date and time

    Returns:
        int: epoch timestamp
    """

    return int(from.timestamp() * 1e3)


def convertFromEpoch(from: int) -> datetime:
    """ Converts epoch (in milliseconds) to human-readable date and time.

    Args:
        time (int): epoch timestamp

    Returns:
        datetime: date and time
    """

    return datetime.datetime.fromtimestamp((from / 1000.0)).strftime('%Y-%m-%d %H:%M:%S.%f')

