
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
    timestamp: int = datetime.datetime.now().timestamp()
    currency: str = 'USD'
    weight: str = "oz"
    element: str = "au"
    source: str = None

    def __str__(self):
        return f"${round(self.price, 2):.2f}/{self.weight} {self.currency}"


""" Functions that make API calls to get metal price
"""
def metal_price(target, currency: str="USD", metal_type: str='au') -> MetalPrice:
    """ Checks a couple apis and gives metal price nearest target date

        Only one source is checked for silver price.

    Args:
        target (datetime): 
        currency (str): 
        metal_type (str): 

    Returns:
        MetalPrice: Package with details regarding metal price
    """
    
    times = timeRange(target)
    fgpn = fetchGoldPriceNow(currency)
    fgo = fetchGoldOrg(times[0], times[1], currency)
    prices = fgpn + fgo # And any other additional API calls

    if metal_type in ("silver", "ag") and fgpn[1].element == "ag":
        return fgpn[1]

    n = nearestTime(target, prices)

    if n.currency != currency:
        print(f'Failed to obtain gold price in {currency} from "{n.source}"; switched to {n.currency}.')
        
    return n


def fetchGoldPriceNow(currency: str="USD"):
    """ Fetch current gold price from goldprice.org

    Args:
        None

    Raises:
        ErrorAcquireMetalData: When failed to retrieve metal data

    Returns:
        data (list): dataclass with metal price and relevant information
    """

    site = "goldprice.org"
    url = f"https://data-asg.goldprice.org/dbXRates/{currency}"

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0'
    }

    results = requests.get(url, headers=headers).json()   
    if not results:
        raise ErrorAcquireMetalData(f" [ERROR] No data retrieved from {site}")
        sys.exit(-1)
    elif not results['items']:
        url = f"https://data-asg.goldprice.org/dbXRates/USD"
        results = requests.get(url, headers=headers).json()

        if not results:
            raise ErrorAcquireMetalData(f" [ERROR] No data retrieved from {site}")
            return []
            # sys.exit(-1)

    data = [
        MetalPrice(round(results['items'][0]['xauPrice'], 2), results['tsj'], results['items'][0]['curr'], source=site),
        MetalPrice(round(results['items'][0]['xagPrice'], 2), results['tsj'], results['items'][0]['curr'], element='ag', source=site)
    ]

    return data

def fetchGoldOrg(start, end, currency: str="USD", weight: str="oz"):
    
    site = "gold.org"
    url = f"https://fsapi.gold.org/api/goldprice/v11/chart/price/{currency}/{weight}/{start},{end}"

    res = requests.get(url).json()
    if not res:
        raise ErrorAcquireMetalData(f" [ERROR] No data retrieved from {site}")
    
    if currency.upper() == (curr:= list(res['chartData'].keys())[0].upper()):
        curr = currency

    try:
        if len(curr) != 3:
            raise ValueError("Unable to get correct currency key.")

        data = [ MetalPrice(round(el[1], 2), el[0], curr, weight, source=site) for el in res['chartData'][curr] ]
    except ValueError as e:
        # print(e)
        return []
    except KeyError as e:
        print(" [ERROR] Issue with JSON key.")
        sys.exit(-1)

    return data

