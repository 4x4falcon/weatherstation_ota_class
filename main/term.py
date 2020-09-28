help = """
showWSConfig()				- show current configuration
showSleepDelay()			- show the current time interval for readings in milliseconds
setSleepDelay(<milliseconds>)		- set the time interval for readings in milliseconds (default 60000 - 1 min)
showBatteryVoltage()			- show the current battery rated voltage
setBatteryVoltage(<battervoltage>)	- set the battery rated voltage (default 3.7V)
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


def showSleepDelay():
	with open(config_file) as cf:
		config = json.load(cf)
	print ("Sleep delay: ", config['config']['sleepdelay'])

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



def showBatteryVoltage():
	with open(config_file) as cf:
		config = json.load(cf)
	print ("Battery voltage: ", config['config']['batteryvoltage'])

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

