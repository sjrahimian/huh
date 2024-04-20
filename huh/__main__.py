#!/usr/bin/env python

""" This is MAIN
"""

# Standard library
import sys
from datetime import datetime
from pathlib import Path
import ssl
import logging

# 3rd Party Library
from currency_converter import CurrencyConverter, SINGLE_DAY_ECB_URL

# cfg_local imports
from huh.settings import arguments, Configuration
from huh.huquq import Huququllah, HuququLabels, record
from huh.metal import metal_price, MetalPrice
import huh.spacetime as st

def floatFmt(*args):
    return [ f'{round(x, 2):.2f}' for x in args ]

def mp_wrapper(tt, usrPrice=None, curr=None):
    if usrPrice:
        curr, prc, unt = usrPrice.split(",")
        val = MetalPrice(price=float(prc), currency=curr, weight=unt.lower(), source="user")
    elif curr:
        val = metal_price(tt, curr)
    else:
        val = metal_price(tt)
    
    return val

def convertPrice(price, currFrom, currTo):
    val = False
    if not val:
        ssl._create_default_https_context = ssl._create_unverified_context
        c = CurrencyConverter(SINGLE_DAY_ECB_URL)
        try:
            val = c.convert(price, currFrom.upper(), currTo.upper())
        except ValueError as e:
            print(e)
            sys.exit(1)

    return val

# Run
def run():
    try:
        args = arguments()
        print(args)
        print("\n\n")
        cfg = None #Configuration("huq.ini").conf
    except ValueError as e:
        print(e)
        sys.exit(-1)
    
    if not cfg:
        dateTmp = datetime.strptime("04-20", "%m-%d")
        dateTmp = st.fixFiscalDate(dateTmp)
        timeTmp = st.getSolarTime(date=dateTmp)
        target_time = datetime.combine(dateTmp, timeTmp.time())
        m = mp_wrapper(target_time, args.price)


    else:
        # Determine time period for when gold prices should be gathered
        cfg_loc = cfg['LOCATION']
        fiscalDate, fiscalTime =  datetime.strptime(cfg['FISCAL']['date'], "%m-%d"), cfg['FISCAL']['time']
        fiscalDate = st.fixFiscalDate(fiscalDate)

        if (period:= fiscalTime.lower().rstrip()) in st.getSunPeriodTerms():
            address = f"{cfg_loc['city']} {cfg_loc['state']} {cfg_loc['country']}"      
            timeTmp = st.getSolarTime(address, cfg_loc['latitude'], cfg_loc['longitude'], period, fiscalDate)
            target_time = datetime.combine(fiscalDate, timeTmp.time())
        elif fiscalTime.lower().rstrip() == 'now':
            target_time = datetime.now()
        else:
            target_time = datetime.combine(fiscalDate, datetime.strptime(fiscalTime, "%H:%M").time())

        # Fetch the price of gold
        c = args.curr.upper() if args.curr else cfg['HUQUQ']['currency'].upper()
        m = mp_wrapper(target_time, args.price, c)


    # Convert for currency and weight
    if cfg['HUQUQ']['currency'].upper() != m.currency and args.curr != m.currency:
        curr = args.curr if args.curr else cfg['HUQUQ']['currency']
        print(f"Original gold price ({m.source}): {m}")
        m = MetalPrice(timestamp=m.timestamp, price=convertPrice(m.price, m.currency, curr), currency=curr.upper(), weight=m.weight, source=m.source + " (pre-conversion)")
        print(f"Equivalent gold price ({m.source}): {m}")

    # Calculate tax
    huq = Huququllah(args.amount, m.price, m.weight)
    # print(">>1>", huq.basic)

    if args.basic:
        huq.basic = args.basic
        huq._remainder()
        huq._payable()
        # print(">>2>", huq.basic)
    
    # Full output
    if args.detail:
        if not args.price:
            print(f'Date & time for price search: {target_time}')
            print(f'Date & time for gold price: {st.epochToDatetime(m.timestamp)}')
        print(f"Gold price ({m.source}): {m}")
        print(" ~ ~ ~ ")
        huq.report()
    else:
        print(m)
        print(huq)

    # Record: created date, retrieved date, metal price, metal weight, metal currency, wealth, payable
    if 'file' in cfg['CSV']:
        pkg = [datetime.now(), target_time] + floatFmt(m.price)+ [m.weight, m.currency, m.source] + floatFmt(huq.wealth, huq.payable)
        if (f:= Path(cfg['CSV']['file'])).is_dir():
            record(f, pkg)
        else:
            record(Path(FAIL.CSV), pkg)