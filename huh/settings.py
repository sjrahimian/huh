#!/usr/bin/env python

""" Settings for the project.

Load the customizable settings defined in 'config.ini', and setup the logger settings.

""" 

# Standard library
import argparse
from datetime import datetime
import re
import configparser
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

# Local Imports
from huh.__init__ import __title__
from .huquq import HuququLabels

class IncorrectConfigValue(ValueError):
    """ Incorrect value exception class for errors from this module. """

class MissingConfigValue(ValueError):
    """ Missing value exception class for errors from this module. """


class Configuration():
    def __init__(self, file, log=Path("app.log")):
        self.file = Path(file)
        self.config = self._load()
        self.validateConfig(self.config)
        # self._prepareLogger(log)
    
    @property
    def conf(self):
        return self.config

    def _load(self):
        try:
            if not self.file.is_file():
                raise FileNotFoundError(f"Could not find {self.file} file.")
            else:
                temp = configparser.ConfigParser()
                temp.read(self.file)
                return temp
            
        except FileNotFoundError as e:
            print(f"[ERROR] {e}")
            sys.exit(-1)

    def validateConfig(self, cfg):
        
        # Are there any empty keywords
        for section in cfg:
            for key in cfg[section]:

                if section != "LOCATION":
                    if cfg[section][key] == "":
                        raise MissingConfigValue(f"Missing value for: [{section}] > {key}")

        # Special case 
        section = 'LOCATION'
        loc = cfg[section]
        if (loc['city'] == "" or loc['country'] == "") and (loc['latitude'] == "" or loc['longitude'] == ""):
            raise MissingConfigValue(f'Missing value for: [{section}].\nAdd either address or latitude/longitude.')                        
        
        # Check values
        section = 'FISCAL'
        val = cfg[section]['time']
        if val not in ('dawn', 'sunrise', 'noon', 'sunset', 'dusk', 'now'):
            if not re.fullmatch("[0-9][0-9]:[0-9][0-9]", val):
                raise IncorrectConfigValue(f'[{section}] > time value is invalid: "{val}"')
                sys.exit(1)
            try:
                datetime.strptime(val, "%H:%M")
            except ValueError:
                print(f'[{section}] > time value is not a valid 24-hour format: "{val}"')
                sys.exit(1)

        val = cfg[section]['date']
        if not re.fullmatch("[0-1][0-9]-[0-3][0-9]", val):
            raise IncorrectConfigValue(f'[{section}] > date value is invalid: "{val}"')
            sys.exit(1)

        try:
            datetime.strptime(val, "%m-%d")
        except ValueError:
            print(f'[{section}] > fiscal date value is not a valid "MM-DD" format: "{val}"')
            sys.exit(1)

    # Logger setup for use throughout application
    def _prepareLogger(self, fn):
        try:
            # rotating files saves time and manual clean-up
            handler = RotatingFileHandler(filename=fn)
            
            # define how logger should output
            logging.basicConfig(format='%(message)s', 
                level=logging.INFO, handlers=[handler])

        except Exception as e:
            print(f"Error in logger settings: \n{e}")
            sys.exit(-1)


class MetalPriceAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values and not re.fullmatch("([a-zA-Z]{3}),([0-9]+.?[0-9]{0,2}),(troy\soz|t\soz|toz|oz|grams|gram|g){1}", values):
                raise ValueError("Incorrect format for custom gold price: '[currency],[price],[weight]'\n(e.g., 'usd,1,troy oz)'\n")

        setattr(namespace, self.dest, values)

def arguments():
    parser = argparse.ArgumentParser(description=f'Help calculate {HuququLabels.diacritic_upper} tax by retrieving the price of gold and performing the required operations.', epilog=f"The program will output the gold price and any payable amount of {HuququLabels.diacritic_lower}.")

    parser.add_argument('amount', type=float, help=f'The amount of wealth after expenses to pay {HuququLabels.name} on.')
    parser.add_argument('-b', '--basic', type=float, default=None, help=f'One basic unit equal to 19 {HuququLabels.mithqal}.')
    parser.add_argument('-c', '--curr', type=str, default=None, help=f'Convert currency (overrides configuration file).')
    parser.add_argument('-d', '--detail', action='store_true', help='Detailed output.')
    parser.add_argument('-p', '--price', type=str, action=MetalPriceAction, default=None, help="Provide the gold price: '[currency],[price],[weight]'.")

    return parser.parse_args()
