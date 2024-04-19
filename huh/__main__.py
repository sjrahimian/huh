#!/usr/bin/env python

""" This is MAIN
"""

# Standard library
import sys
from datetime import datetime
from pathlib import Path

import logging

# 3rd Party Library

# cfg_local imports
from huh.settings import arguments, Configuration
from huh.huquq import Huququllah, HuququLabels, record
from huh.metal import metal_price, MetalPrice
import huh.spacetime as st


def floatFmt(*args):
    return [ f'{round(x, 2):.2f}' for x in args ]

def mp_wrapper(usrPrice, tt):
    if usrPrice:
        cur, prc, unt = usrPrice.split(",")
        val = MetalPrice(price=float(prc), currency=cur.upper(), weight=unt.lower(), source="user")
    else:
        val = metal_price(tt)
    
    return val

# Run
def run():
    try:
        args = arguments()
        print(args)
        print("\n\n")
        cfg = Configuration("huq.ini").conf
    except ValueError as e:
        print(e)
        sys.exit(-1)

    
    if not cfg:
        dateTmp = datetime.strptime("04-20", "%m-%d")
        dateTmp = st.fixFiscalDate(dateTmp)
        timeTmp = st.getSolarTime(date=dateTmp)
        target_time = datetime.combine(dateTmp, timeTmp)
        m = mp_wrapper(args.price, target_time)


    else:
        # Determine time period for when gold prices should be gathered
        cfg_loc = cfg['LOCATION']
        fiscalDate, fiscalTime =  datetime.strptime(cfg['FISCAL']['date'], "%m-%d"), cfg['FISCAL']['time']
        fiscalDate = st.fixFiscalDate(fiscalDate)

        print(fiscalTime.lower())
        if (period:= fiscalTime.lower().rstrip()) in st.getSunPeriodTerms():
            address = f"{cfg_loc['city']} {cfg_loc['state']} {cfg_loc['country']}"      
            timeTmp = st.getSolarTime(address, cfg_loc['latitude'], cfg_loc['longitude'], period, fiscalDate)
            target_time = datetime.combine(fiscalDate, timeTmp.time())
        elif fiscalTime.lower().rstrip() == 'now':
            target_time = datetime.now()
            print("????", target_time)
        else:
            target_time = datetime.combine(fiscalDate, datetime.strptime(fiscalTime, "%H:%M").time())

        # Fetch the price of gold
        m = mp_wrapper(args.price, target_time)


    # Calculate huququllah
    huq = Huququllah(args.amount, m.price, m.weight)
    print(">>",huq.basic)


    # print(huq)
    if args.basic:
        huq.basic = args.basic
        huq._remainder()
        huq._payable()
        print(">>",huq.basic)
    

    # print(huq.payable)

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

    # Calculate and convert for currency and weight



    # Record: created date, retrieved date, metal price, metal weight, metal currency, wealth, payable
    pkg = [datetime.now(), target_time] + floatFmt(m.price)+ [m.weight, m.currency, m.source] + floatFmt(huq.wealth, huq.payable)
    if (f:= Path(cfg['CSV']['file'])).is_dir():
        record(f, pkg)
    else:
        record(pkg)