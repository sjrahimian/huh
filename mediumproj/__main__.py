#!/usr/bin/env python

""" This is MAIN
"""

# Standard library
from datetime import datetime, timedelta
import sys
# import logging

# 3rd Party Library

# Local imports
from mediumproj.settings import CONFIGURE
from mediumproj.goodbye import bye

# Run
def run():
	start = datetime.today()
	# logger = logging.getLogger(__name__)

		# some sample code
	print("In the __main__ file")
	print("Environment: ", CONFIGURE['DEFAULT']['enviro'])
		
	try:
		print("================= function calls =================")
		bye.bye()
		bye.call_settings_from_bye()
		print("================= done =================")
		bye.house()
	except Exception as e:
		print("\n\t Failed intentionally:")
		print(e)
		sys.exit(-1)

	finally:
		diff = datetime.today() - start
		# logger.info(f"Completed,start:{start},end:{datetime.today()},duration:{diff.days} {timedelta(seconds=diff.seconds)}")
		sys.exit(1)
