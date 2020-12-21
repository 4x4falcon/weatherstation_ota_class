help = """
c10()		=	showWSConfig()				- show current configuration
c11()		=	showSleepDelay()			- show the current time interval for readings in milliseconds
c12(<ms>)	=	setSleepDelay(<milliseconds>)		- set the time interval for readings in milliseconds (default 60000 - 1 min)
c13()		=	showBatteryVoltage()			- show the current battery rated voltage
c14(<volt>)	=	setBatteryVoltage(<battervoltage>)	- set the battery rated voltage (default 3.7V)
c15()		=	showVersion()				- show current installed version

c20()		=	calibrateOn()				- turn on calibrate mode
c21()		=	calibrateOff()				- turn off calibrate mode
"""

print (help)

import json

config_file = 'ws/main/config/config.json'

def showWSConfig():
	with open(config_file) as cf:
		config = json.load(cf)
	print ("Outside: ", config['config']['outside'])
	print ("Calibrate: ", config['config']['calibrate'])
	print ("Battery voltage: ", config['config']['batteryvoltage'])
	print ("Sleep delay: ", config['config']['sleepdelay'])

def c10():
	showWSConfig()

def showSleepDelay():
	with open(config_file) as cf:
		config = json.load(cf)
	print ("Sleep delay: ", config['config']['sleepdelay'])

def c11():
	showSleepDelay()

def setSleepDelay(ms=60000):

	if (ms != None) and (ms > 0):
		try:
		        with open(config_file) as cf:
		                config = json.load(cf)
		        print ("Current Sleep Delay: ", config['config']['sleepdelay'])
			config['config']['sleepdelay'] = ms
			print ("New Sleep Delay: ", config['config']['sleepdelay'])
			with open(config_file, 'w') as cf:
				json.dump(config, cf)
		except OSError:
	                print ("No config file at ", config_file)
		except Exception:
			print ("Error occured")
	else:
		print ("Nothing to change")

def c12(ms=60000):
	setSleepDelay(ms)


def showBatteryVoltage():
	with open(config_file) as cf:
		config = json.load(cf)
	print ("Battery voltage: ", config['config']['batteryvoltage'])

def c13():
	showBatteryVoltage()

def setBatteryVoltage(bv=3.7):

	if (bv != None) and (bv > 0):
		try:
		        with open(config_file) as cf:
		                config = json.load(cf)
		        print ("Current Battery Voltage: ", config['config']['batteryvoltage'])
			config['config']['batteryvoltage'] = bv
			print ("New Battery Voltage: ", config['config']['batteryvoltage'])
			with open(config_file, 'w') as cf:
				json.dump(config, cf)
		except OSError:
	                print ("No config file at ", config_file)
		except Exception:
			print ("Error occured")
	else:
		print ("Nothing to change")

def c14(bv=3.7):
	setBatteryVoltage(bv)


def showVersion():
	f=open('ws/main/.version')
	print(f.read())
	f.close()

def c15():
	showVersion()



def calibrateOn():

	try:
	        with open(config_file) as cf:
	                config = json.load(cf)
	        print ("Calibrate mode: ", config['config']['calibrate'])
		config['config']['calibrate'] = 1
		print ("New calibrate mode: ", config['config']['calibrate'])
		with open(config_file, 'w') as cf:
			json.dump(config, cf)
	except OSError:
                print ("No config file at ", config_file)
	except Exception:
		print ("Error occured")

def c20():
	calibrateOn()

def calibrateOff():

	try:
	        with open(config_file) as cf:
	                config = json.load(cf)
	        print ("Calibrate mode: ", config['config']['calibrate'])
		config['config']['calibrate'] = 0
		print ("New calibrate mode: ", config['config']['calibrate'])
		with open(config_file, 'w') as cf:
			json.dump(config, cf)
	except OSError:
                print ("No config file at ", config_file)
	except Exception:
		print ("Error occured")

def c21():
	calibrateOff()
