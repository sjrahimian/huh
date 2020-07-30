
from mediumproj.settings import CONFIGURE


def bye():
	print("Goodbye World")

def call_settings_from_bye():
	print(f"also in {CONFIGURE['DEFAULT']['enviro']} mode")

