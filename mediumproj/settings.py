#!/usr/bin/env python

""" Settings for the project.

Load the customizable settings defined in 'config.ini', and setup the logger settings.

""" 

# Standard library
import configparser
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys



def __load__(file):
	try:
		if not file.is_file():
			raise FileNotFoundError("Could not find file; missing 'config.ini'.")
		else:
			temp = configparser.ConfigParser()
			temp.read(file)
			return temp
		
	except FileNotFoundError as e:
		print(f"Configuration __load__ error: {e}\n 'file': {file}\n")
		sys.exit(-1)

INI_FILE = Path('config.ini')
CONFIGURE = __load__(INI_FILE)


# Logger setup for use throughout application
def __prepLogger__(cnfg):
	try:

		# rotating files saves time and manual clean-up
		handler = RotatingFileHandler(filename=(Path(cnfg["LOGGER"]["path"], cnfg["LOGGER"]["filename"])), 
			maxBytes=int(cnfg["LOGGER"]["max bytes"]), 
			backupCount=int(cnfg["LOGGER"]["historical count"]))

		# create logger for development or production
		if cnfg["DEFAULT"]["enviro"].lower() == "development":
			logging.basicConfig(format='%(asctime)s; %(levelname)s; %(name)s; %(message)s', 
				level=logging.DEBUG,
				handlers=[handler])
			logging.debug("Application started in development mode; level=logging.DEBUG")
		else:
			logging.basicConfig(format='%(asctime)s; %(levelname)s; %(name)s; %(message)s', 
				level=logging.INFO,
				handlers=[handler])
			logging.info("Application started in production mode; level=logging.INFO")
			
	except Exception as e:
		print(f"Error in logger settings: \n{e}")
		sys.exit(-1)


# Prepare logger
__prepLogger__(CONFIGURE)

