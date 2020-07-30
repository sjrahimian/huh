from mediumproj.settings import CONFIGURE
from mediumproj.goodbye import bye

# Run
def run():
	try:
		# some sample code
		print("In the __main__ file")
		
		print("Environment: ", CONFIGURE['DEFAULT']['enviro'])
		
		bye.bye()
		print("=================")
		bye.call_settings_from_bye()
		
	except Exception as e:
		print("\n\nFailed in app.py")
		print(e)
		

