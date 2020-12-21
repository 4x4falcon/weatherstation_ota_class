# -------------------------------------------------------------------------------

from machine import Pin, I2C, RTC, reset
from time import sleep, sleep_ms

# uncomment when debugging callback problems
import micropython
micropython.alloc_emergency_exception_buf(100)

from .classes.bme280 import *
from .classes.debounce import DebouncedSwitch

print("imported classes")

import utime

import urequests

#import machine

import json

# load config

config = None

try:
        with open('ws/main/config/config.json') as cf:
                config = json.load(cf)

except Exception:
	print("not on ota")

else:
	try:
        	with open('config/config.json') as cf:
                	config = json.load(cf)
	except Exception:
		pass

outside = config['config']['outside']
calibrate = int(config['config']['calibrate'])

# import my functions
from .functions import *

# select esp32 or esp8266

esp32 = setEsp32()


if (esp32):
#	sw1 = DebouncedSwitch(Pin(5, Pin.IN, Pin.PULL_UP), interrupt_cb, "w", delay=30)
#	sw2 = DebouncedSwitch(Pin(17, Pin.IN, Pin.PULL_UP), interrupt_cb, "r", delay=30)

	sw1 = DebouncedSwitch(Pin(18, Pin.IN, Pin.PULL_UP), windspeed_cb, "w", delay=30, tid=4)

#	sw1 = DebouncedSwitch(Pin(5, Pin.IN, Pin.PULL_UP), windspeed_cb, "w", delay=30, tid=4)
	sw2 = DebouncedSwitch(Pin(17, Pin.IN, Pin.PULL_UP), rainfall_cb, "r", delay=30, tid=3)
else:
	sw1 = DebouncedSwitch(Pin(15, Pin.IN, Pin.PULL_UP), interrupt_cb, "w", delay=30)
	sw2 = DebouncedSwitch(Pin(0, Pin.IN, Pin.PULL_UP), interrup_cb, "r", delay=30)

#print("set interrupts")


# total time between loops in microseconds
sleepdelay = int(config['config']['sleepdelay'])
if (calibrate == 1):
	sleepdelay = 5000

print ("Sleepdelay: ", sleepdelay)

# offset for epoch time from 1-1-1970 to 1-1-2000
epochoffset = 946684800

# battery voltage
batteryvoltage = float(config['config']['batteryvoltage'])

# inbuilt led
led = Pin(2, Pin.OUT)
led.off()

# Freetronics hardware watchdog pin
if (esp32):
# ESP32 - Pin assignment
	Hwwd = Pin(23, Pin.OUT)
else:
# ESP8266 - Pin assignment
	Hwwd = Pin(13, Pin.OUT)

from .classes.freetronicsWatchdog import Watchdog
watchdog = Watchdog(Hwwd)


# load wifi config

wifi_cfg = None

try:
        with open('config/wifi_cfg.json') as cf:
                wifi_cfg = json.load(cf)
        print ("SSID: ", wifi_cfg['wifi']['ssid'])
        print ("PW: ", wifi_cfg['wifi']['password'])
	print ("Hostname: ", wifi_cfg['wifi']['hostname'])

except Exception:
                pass

# connect to wifi
do_connect(wifi_cfg['wifi']['ssid'], wifi_cfg['wifi']['password'], wifi_cfg['wifi']['hostname'])

rtc = RTC()
# synchronize with ntp
# need to be connected to wifi

print("get ntp time")

import ntptime

tries = 10
for i in range(tries):
	try:
		ntptime.host = config['config']['ntphost']
		ntptime.settime() 	# set the rtc datetime from the remote server
		rtc.datetime()    	# get the date and time in UTC
	except:
		if i < tries - 1: # i is zero indexed
			print(".")
			sleep_ms(10000)
			continue
	break

setntpset(utime.time() + epochoffset)
#print("ntpset: ", getntpset())

if (esp32):
# ESP32 - Pin assignment
	i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
else:
# ESP8266 - Pin assignment
	i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)


# main loop

try:
	while True:

# start of loop time
		loopstart = utime.ticks_ms()

		toggle(led)

		watchdog.feed()

		timestamp = utime.time() + epochoffset

		# reconnect to wifi if disconnected
		if not wlan.isconnected():
			do_connect(wifi_cfg['wifi']['ssid'], wifi_cfg['wifi']['password'], wifi_cfg['wifi']['hostname'])

# update ntp time every 30 minutes 1800 seconds
		if (resetntp(timestamp)):
			for i in range(tries):
				try:
					ntptime.host = config['config']['ntphost']
					ntptime.settime() 			# set the rtc datetime from the remote server
					rtc.datetime()    			# get the date and time in UTC
					timestamp = utime.time() + epochoffset
					print('Updating time via ntp')
				except:
					if i < tries - 1: 			# i is zero indexed
						sleep_ms(10000)
						print(".")
						continue
				break

		try:
			bme280 = BME280(i2c=i2c)

			t, p, h = bme280.values

			temp = str(t).replace("C", "")
			hum = str(h).replace("%", "")
			pres = str(p).replace("hPa", "")

			print ("removed units")


# calculate dew point

#			from math import log
#		        hum = (log(hum, 10) - 2) / 0.4343 + (17.62 * temp) / (243.12 + temp)
#		        dew = 243.12 * hum / (17.62 - hum)

#			dew = bme280.dew_point
			dew = 0.0

		except:
			print('No bme280 present')
			temp = -99
			hum = -99
			pres = -99
			dew = -99



# read battery voltage
		volt = getBatteryVoltage(batteryvoltage)

		winddir = getWinddir()

		ws = getWindspeed()
		rf = getRainfall()

		if (outside):
			data = 'ti=' + str(timestamp) + '&t=' + str(temp) + '&p=' + str(pres) + '&h=' + str(hum) + '&v=' + str(volt) + '&rf=' + str(rf) + '&ws=' + str(ws) + '&wd=' + str(winddir) + '&d=' + str(dew)
		else:
			data = 'ti=' + str(timestamp) + '&t=' + str(temp) + '&p=' + str(pres) + '&h=' + str(hum) + '&v=' + str(volt) + '&rf=' + str(rf) + '&rl=' + '0.0'

		ws = 0
		rf = 0

		print ('Data: ', data)

		serverurl = config['config']['serverurl']

		try:
			if (outside == '1'):
				headers = {'User-Agent': 'uP-esp32devkitpro', 'Content-Type': 'application/x-www-form-urlencoded'}
#				response = urequests.post("http://10.0.0.33/status/weather/espdata_outside.php", data=data, headers=headers)
				response = urequests.post(serverurl, data=data, headers=headers)
				print('Response: ', response.text)
			else:
				headers = {'User-Agent': 'uP-esp32devkitpro', 'Content-Type': 'application/x-www-form-urlencoded'}
#				response = urequests.post("http://10.0.0.33/status/weather/espdata.php", data=data, headers=headers)
				response = urequests.post(serverurl, data=data, headers=headers)
				print('Response: ', response.text)
		except:
			continue

# Go to sleep for the specified time (minus the time we needed for all the stuff we did in the loop)

		loopend = utime.ticks_ms()

		realdelay = sleepdelay + utime.ticks_diff(loopstart, loopend)

#	print("Realdelay: ", realdelay)

		sleep_ms(realdelay)

		if (response.text == '99'):
			file = open("doUpdate","w")
			file.write(str(response.text))
			file.close()
			machine.reset()


except KeyboardInterrupt:
	print('Caught Control-C')

