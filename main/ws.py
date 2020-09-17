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

		self.led.value(not self.led.value())

