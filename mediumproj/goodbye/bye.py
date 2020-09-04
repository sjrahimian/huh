#!/usr/bin/env python

""" Short description.

Lllloooooonnnnnngggggggg    d e s c r i p t i o n.
	
""" 

# Standard library

# 3rd Party Library

# Local imports
from mediumproj.settings import CONFIGURE


def bye():
	print("Goodbye World")

def call_settings_from_bye():
	print(f"also in {CONFIGURE['DEFAULT']['enviro']} mode")

