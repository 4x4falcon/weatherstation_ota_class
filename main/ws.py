#! /usr/bin/env python
#
# Weather Station OTA class
#
# MIT License
#
# Copyright (c) 2020 Ross Scanlon <info@4x4falcon.com>
#
# based on MicroPython OTA Updater Example Module
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Weather Station OTA Class"""

from machine import Pin
import utime

# setup freetronics watchdog
# Freetronics hardware watchdog pin
Hwwd = Pin(5, Pin.OUT)

from classes import Watchdog
#from classes.freetronicsWatchdog import Watchdog
watchdog = Watchdog(Hwwd)

# offset for epoch time from 1-1-1970 to 1-1-2000
epochoffset = 946684800


class WeatherStationClass:
	"""Weather Station Class"""

	def __init__(self):
		self.led = Pin(2, Pin.OUT)
		pass

	def __call__(self):
		return self

	def do_it(self):
		"""This is the main loop of the class"""
		print("Hello from Weather Station Class.")

		while True:

			self.led.value(not self.led.value())

# start of loop time
			loopstart = utime.ticks_ms()


# Go to sleep for the specified time (minus the time we needed for all the stuff we did in the loop)

			loopend = utime.ticks_ms()

			realdelay = sleepdelay + utime.ticks_diff(loopstart, loopend)

			sleep_ms(realdelay)

			watchdog.feed()

			timestamp = utime.time() + epochoffset

# update ntp time every 30 minutes 1800 seconds

			if (f.resetntp(timestamp)):

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



"""
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

# read battery voltage from A0
	volt = f.getBatteryVoltage(batteryvoltage)

	winddir = f.getWinddir()

	if (outside):
		data = 'ti=' + str(timestamp) + '&t=' + str(temp) + '&p=' + str(pres) + '&h=' + str(hum) + '&v=' + str(volt) + '&rf=' + str(f.rf) + '&ws=' + str(f.ws) + '&wd=' + str(winddir)
 + '&d=' + str(dew)
	else:
		data = 'ti=' + str(timestamp) + '&t=' + str(temp) + '&p=' + str(pres) + '&h=' + str(hum) + '&v=' + str(volt) + '&rf=' + str(f.rf) + '&rl=' + '0.0'

# zero interrupt counters
	f.ws = 0
	f.rf = 0

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
"""
