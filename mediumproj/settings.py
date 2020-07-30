# 
import os, sys
import configparser


def load(file):
	try:
		if not os.path.isfile(file):
			raise FileNotFoundError("Could not find file; missing 'config.ini'.")
		else:
			temp = configparser.ConfigParser()
			temp.read(file)
			return temp
		
	except FileNotFoundError as e:
		print(f"Configuration load error: {e}\n 'file': {file}\n")
		sys.exit(-1)

INI_FILE = 'config.ini'
CONFIGURE = load(INI_FILE)
