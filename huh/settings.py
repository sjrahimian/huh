#!/usr/bin/env python

""" Settings for the project.

Load the customizable settings defined in 'config.ini', and setup the logger settings.

""" 

# Standard library
import argparse
import re
import configparser
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

from huh.__init__ import __title__

class IncorrectConfigValue(ValueError):
    """ Incorrect value exception class for errors from this module. """

class MissingConfigValue(ValueError):
    """ Missing value exception class for errors from this module. """


class Configuration():
    def __init__(self, file, log):
        self.file = Path(file)
        self.config = self._load()
        self.validateConfig(self.config)
        if log:
            self._prepareLogger(Path(self.config['LOGGER']['filename']))
    
    @property
    def conf(self):
        return self.config

    def _load(self):
        try:
            if not self.file.is_file():
                raise FileNotFoundError("Could not find file; missing 'config.ini'.")
            else:
                temp = configparser.ConfigParser()
                temp.read(self.file)
                return temp
            
        except FileNotFoundError as e:
            print(f"[ERROR] {e}\n 'file': {self.file}\n")
            sys.exit(-1)

    def validateConfig(self, cfg):
        
        # Are there any empty keywords
        for section in cfg:
            for key in cfg[section]:

                if section != "LOCATION":
                    if cfg[section][key] == "":
                        raise MissingConfigValue(f"Missing value for: [{section}] > {key}")                        

        # Special case 
        loc = cfg['LOCATION']
        if (loc['city'] == "" or loc['country'] == "") and (loc['latitude'] == "" or loc['longitude'] == ""):
            raise MissingConfigValue(f'Missing value for: [LOCATION].\nAdd either address or latitude/longitude.')                        
        
        # Check values
        val = cfg['HUQUQ']['metal']
        if val not in ('silver', 'gold'):
            raise IncorrectConfigValue(f'[HUQUQ] > metal value is invalid: "{val}"')

        val = cfg['HUQUQ']['unit']
        if val not in ('name', 'diacritic', 'short', 'symbol'):
            raise IncorrectConfigValue(f'[HUQUQ] > unit value is invalid: "{val}"')
        
        val = cfg['DATETIME']['time']
        if val not in ('dawn', 'sunrise', 'noon', 'sunset', 'dusk', 'now'):
            if not re.fullmatch("[0-9][0-9]:[0-9][0-9]", val):
                raise IncorrectConfigValue(f'[DATETIME] > time value is invalid: "{val}"')
                sys.exit(1)
            try:
                dt.datetime.strptime(val, "%H:%M")
            except ValueError:
                print(f'[DATETIME] > time value is not a valid time in 24-hour notation: "{val}"')
                sys.exit(1)


    # Logger setup for use throughout application
    def _prepareLogger(self, fn):
        try:
            # rotating files saves time and manual clean-up
            handler = RotatingFileHandler(filename=fn)
            
            # define how logger should output
            logging.basicConfig(format='%(asctime)s; %(levelname)s; %(name)s; %(message)s', 
                level=logging.INFO,
                handlers=[handler])
            logging.debug("Application started in development mode; level=logging.DEBUG")

        except Exception as e:
            print(f"Error in logger settings: \n{e}")
            sys.exit(-1)

def arguments():
    parser = argparse.ArgumentParser(prog=f'{__title__}', description='Calculate HQUH')

    parser.add_argument('amount', type=float, help='The amount after expenses to pay HQUH on.')
    parser.add_argument('-u', '--unit', type=float, help='One unit of HQUH (equal to 19 mithqals).')
    parser.add_argument('-p', '--price', type=float, help='Metal price.')
    parser.add_argument('-l', '--log', action='store_true', help='Record to file.')

    return parser.parse_args()
