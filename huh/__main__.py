#!/usr/bin/env python

""" This is MAIN part of the HUH program that handles that calls the other modules.
"""

# Standard library
import sys
from datetime import datetime
from pathlib import Path
import ssl
import logging

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


# Run
def run():
    try:
        args = arguments()
        cfg = Configuration("huq.ini").conf
    except ValueError as e:
        print(e)
        sys.exit(-1)
    
    if not cfg:
        dateTmp = datetime.strptime("04-20", "%m-%d")
        dateTmp = st.fixFiscalDate(dateTmp)
        timeTmp = st.getSolarTime(date=dateTmp)
        target_time = datetime.combine(dateTmp, timeTmp.time())

        c = args.curr.upper() if args.curr else None
        m = mp_wrapper(target_time, args.price, c)

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
        tmpCurr = cfg['HUQUQ']['currency'].upper() if 'currency' in cfg['HUQUQ'] else None
        c = args.curr.upper() if args.curr else tmpCurr
        m = mp_wrapper(target_time, args.price, c)

    if not m:
        print("Unable to obtain gold price. Bye.")
        sys.exit(-1)

    # Calculate tax
    huq = Huququllah(args.amount, m.price, m.weight)

    if args.basic:
        huq.basic = args.basic
        huq._remainder()
        huq._payable()
    
    # Full output
    if args.detail:
        print(f"~~ HUH: {HuququLabels.diacritic_upper} Helper ~~\n")

        if not args.price:
            print(f'Date & time for price search: {target_time}')
            print(f'Date & time for gold price: {st.epochToDatetime(m.timestamp)}')
            print(" ~ ~ ~ ")

        print(f"Gold price ({m.source}): {m}")
        huq.report()
    else:
        print(f"Gold Price: {m}")
        print(f"   Payable: {str(huq)} {m.currency}")

    if cfg:
        # Record: created date, retrieved date, metal price, metal weight, metal currency, wealth, payable
        if 'file' in cfg['RECORD']:
            pkg = [datetime.now(), target_time] + floatFmt(m.price)+ [m.weight, m.currency, m.source] + floatFmt(huq.wealth, huq.payable)
            if (f:= Path(str(cfg['RECORD']['file']))).parent.is_dir():
                record(pkg, f)