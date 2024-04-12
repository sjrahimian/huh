
# -*- coding: utf-8 -*-

""" Metal price for gold and silver.
"""

# Standard library
from dataclasses import dataclass
import datetime
import requests
import sys

# 3rd Party Library
from .spacetime import nearestTime, timeRange


class ErrorMetalData(Exception):
    """ Base exception class for errors from this module. """

class ErrorAcquireMetalData(ErrorMetalData, Exception):
    """ Exception class for errors from trying to get data. """
    
class ErrorMetalDataConvert(ErrorMetalData, Exception):
    """ Exception class for errors from trying to convert the data. """

@dataclass
class MetalPrice:
    """ Dataclass to neatly bundle metal price data
    """

    price: float = 0.00
    timestamp: int = datetime.datetime.now()
    currency: str = 'USD'
    weight: str = "oz"
    element: str = "au"
    site: str = None


""" Functions that make API calls to get metal price
"""
def metal_price(self, target, currency, weight, metal_type) -> MetalPrice:
    """ Checks a couple apis and gives metal price nearest target date

        Only one site is checked for silver price.

    Args:
        target (datetime): 
        currency (str): 
        weight (str): 
        metal_type (str): 

    Returns:
        MetalPrice: Package with details regarding metal price
    """
    times = timeRange(target)
    fgpn = fetchGoldPriceNow(currency)
    fgo = fetchGoldOrg(times[0], times[1], currency, weight)
    prices = fgpn + fgo # Additional APIs

    if metal_type in ("silver", "ag") and fgpn[1].element == "ag":
        return fgpn[1]

    n = nearestTime(target, prices)
    
    return n


def fetchGoldPriceNow(currency: str="USD"):
    """ Fetch current gold price from goldprice.org

    Args:
        None

    Raises:
        ErrorAcquireMetalData: When failed to retrieve metal data

    Returns:
        _type_: _description_
    """
    import requests

    title = "goldprice.org"
    url = f"https://data-asg.goldprice.org/dbXRates/{currency}"

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0'
    }

    results = requests.get(url, headers=headers).json()   
    if not results or not results['items']:
        raise ErrorAcquireMetalData(f" [ERROR] No data retrieved from {title}")

    data = [
        MetalPrice(round(results['items'][0]['xauPrice'], 2), results['tsj'], results['items'][0]['curr'], site=title),
        MetalPrice(round(results['items'][0]['xagPrice'], 2), results['tsj'], results['items'][0]['curr'], element='ag', site=title)
    ]

    print(data)
    return data

def fetchGoldOrg(start, end, currency: str="USD", weight: str="oz"):
    
    # grams or oz

    title = "gold.org"
    url = f"https://fsapi.gold.org/api/goldprice/v11/chart/price/{currency}/{weight}/{start},{end}"

    res = requests.get(url).json()
    if not res:
        raise ErrorAcquireMetalData(f" [ERROR] No data retrieved from {title}")

    data = [ MetalPrice(round(el[1], 2), el[0], currency, weight, site=title) for el in res['chartData'][currency] ]
    return data

