# -------------------------------------------------------------------------------

outside = True
calibrate = False

#wifi info
SSID = 'tihc4'
SSID_P = '168dead861'


from machine import Pin, I2C, RTC
from time import sleep, sleep_ms

from .classes.bme280 import *
from .classes.debounce import DebouncedSwitch

import utime

import urequests

import machine

# import my functions
from .functions import *
#import .functions as f

# select esp32 or esp8266
from os import uname
if (uname().sysname == 'esp8266'):
	esp32 = False
	print ("found esp8266")


if (esp32):
	sw1 = DebouncedSwitch(Pin(23, Pin.IN, Pin.PULL_UP), windspeed_cb, "d", delay=30)
	sw2 = DebouncedSwitch(Pin(18, Pin.IN, Pin.PULL_UP), rainfall_cb, "d", delay=30)
else:
	sw1 = DebouncedSwitch(Pin(14, Pin.IN, Pin.PULL_UP), windspeed_cb, "d", delay=30)
	sw2 = DebouncedSwitch(Pin(0, Pin.IN, Pin.PULL_UP), rainfall_cb, "d", delay=30)



# total time between loops in microseconds
sleepdelay = 60000
if (calibrate):
	sleepdelay = 5000

# offset for epoch time from 1-1-1970 to 1-1-2000
epochoffset = 946684800

# battery voltage
batteryvoltage = 3.7

# inbuilt led
led = Pin(2, Pin.OUT)
led.off()

# Freetronics hardware watchdog pin
if (esp32):
# ESP32 - Pin assignment
	Hwwd = Pin(5, Pin.OUT)
else:
# ESP8266 - Pin assignment
	Hwwd = Pin(15, Pin.OUT)

from .classes.freetronicsWatchdog import Watchdog
watchdog = Watchdog(Hwwd)

# connect to wifi
do_connect(SSID, SSID_P)

rtc = RTC()
# synchronize with ntp
# need to be connected to wifi

import ntptime

tries = 10
for i in range(tries):
	try:
		ntptime.settime() # set the rtc datetime from the remote server
		rtc.datetime()    # get the date and time in UTC
	except:
		if i < tries - 1: # i is zero indexed
			sleep_ms(10000)
			continue
	break

ntpset = utime.time() + epochoffset

if (esp32):
# ESP32 - Pin assignment
	i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
else:
# ESP8266 - Pin assignment
	i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)


# main loop

while True:

# start of loop time
	loopstart = utime.ticks_ms()

	toggle(led)

	watchdog.feed()

	timestamp = utime.time() + epochoffset

# update ntp time every 30 minutes 1800 seconds

	if (resetntp(timestamp)):

		for i in range(tries):
			try:
				ntptime.settime() # set the rtc datetime from the remote server
				rtc.datetime()    # get the date and time in UTC
				timestamp = utime.time() + epochoffset
				print('Updating time via ntp')
			except:
				if i < tries - 1: # i is zero indexed
					sleep_ms(10000)
					continue
			break


	try:
		bme280 = BME280(i2c=i2c)

		t, p, h = bme280.values

		temp = str(t).replace("C", "")
		hum = str(h).replace("%", "")
		pres = str(p).replace("hPa", "")

		dew = bme280.dew_point

#		print ('Dew Point: ', dew)

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

	try:
		if (outside):
			headers = {'User-Agent': 'uP-esp32devkitpro', 'Content-Type': 'application/x-www-form-urlencoded'}
			response = urequests.post("http://10.0.0.34/status/weather/espdata_outside.php", data=data, headers=headers)
			print('Response: ', response.text)
		else:
			headers = {'User-Agent': 'uP-esp32devkitpro', 'Content-Type': 'application/x-www-form-urlencoded'}
			response = urequests.post("http://10.0.0.34/status/weather/espdata.php", data=data, headers=headers)
			print('Response: ', response.text)
	except:
		continue

# Go to sleep for the specified time (minus the time we needed for all the stuff we did in the loop)

	loopend = utime.ticks_ms()

	realdelay = sleepdelay + utime.ticks_diff(loopstart, loopend)

	sleep_ms(realdelay)
