#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" MAIN part of the HUH program that handles that calls the other modules (a.k.a. cli).
"""

# Standard library
import sys
from datetime import datetime
from pathlib import Path
import ssl
import logging

# Local imports
from .__init__ import __title__
from .settings import arguments, Configuration
from .huquq import Huququllah, HuququLabels, record
from .metal import metal_price, MetalPrice
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
def main():
    try:
        args = arguments()
        configFile = args.filename if args.filename else "./huh.ini"
        cfg = Configuration(configFile).conf
    except ValueError as e:
        print(e)
        sys.exit(-1)
    
    if not cfg:
        # dateTmp = datetime.strptime(, "%m-%d")
        dateTmp = st.setAndFixFiscalDate("04-20")
        timeTmp = st.getSolarTime(date=dateTmp)
        target_time = datetime.combine(dateTmp, timeTmp.time())

        target_curr = args.curr.upper() if args.curr else None
        m = mp_wrapper(target_time, args.price, target_curr)

    else:
        # Determine time period for when gold prices should be gathered
        cfg_loc = cfg['LOCATION']
        fiscalDate, fiscalTime = st.setAndFixFiscalDate(cfg['FISCAL']['date']), cfg['FISCAL']['time']

        if (period:= fiscalTime.lower().rstrip()) in st.getSunPeriodTerms():
            address = f"{cfg_loc['city']} {cfg_loc['state']} {cfg_loc['country']}"      
            timeTmp = st.getSolarTime(address, cfg_loc['latitude'], cfg_loc['longitude'], period, fiscalDate)
            target_time = datetime.combine(fiscalDate, timeTmp.time())
        elif fiscalTime.lower().rstrip() == 'now':
            target_time = datetime.now()
        else:
            target_time = datetime.combine(fiscalDate, datetime.strptime(fiscalTime, "%H:%M").time())

        # Fetch the price of gold
        tmpCurr = cfg['HUQUQ']['currency'].upper() if 'currency' in cfg['HUQUQ'] else "USD"
        target_curr = args.curr.upper() if args.curr else tmpCurr
        m = mp_wrapper(target_time, args.price, target_curr)

    if not m:
        print("Unable to obtain gold price. Bye.")
        sys.exit(-1)

    # Check if metal curr matches amount currency (default currency in config) and if not convert
    # if m.currency != target_curr:
    # m.price, m.currency = convert_price(m.price, m.currency, target_curr)

    # Calculate tax
    huq = Huququllah(args.amount, m.price, m.weight, m.currency)

    if args.basic:
        huq.basic = args.basic
        huq._remainder()
        huq._payable()
    
    # Full output
    if args.detail:
        print(f"~~ {__title__} ~~\n")

        if not args.price:
            print(f'Date & time for price search: {target_time}')
            print(f'Date & time for gold price: {st.epochToDatetime(m.timestamp)}')
            print(" ~ ~ ~ ")

        print(f"Gold price (from {m.source}): {m}")
        huq.report()
    else:
        print(f"Gold price (from {m.source}): {m}")
        print(f"   Payable: {str(huq)} {m.currency}")

    # Create record
    headers = ["recorded date", "gold price retrieved date", "gold price", "weight", "currency", "price source", "wealth", "payable"]
    pkg = [datetime.now(), target_time, m.timestamp] + floatFmt(m.price)+ [m.weight, m.currency, m.source] + floatFmt(huq.wealth, huq.payable)
    if cfg:
        if 'file' in cfg['RECORD']:
            if (f:= Path(cfg['RECORD']['file'])).parent.is_dir():
                record(pkg, f)
    else:
        if args.output:
            if (f:= Path(args.output)).parent.is_dir():
                record(pkg, f)

""" Launch app """
if __name__ == '__main__':
    main()
    sys.exit(0)

""" 
    huh: huququ'llah helper 
    Copyright (C) 2024, Sama Rahimian. All rights reserved.

    This Source Code Form is subject to the terms of the Mozilla
    Public License, v. 2.0. If a copy of the MPL was not distributed
    with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. In no world,
    this or the next, shall the Author be held liable for any
    damages, loss, damnation, or miscalculations, arising from the use
    of this software.

"""

