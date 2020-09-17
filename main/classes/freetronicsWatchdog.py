from time import sleep_ms

class Watchdog:
	def __init__(self, pin):
		self.pin = pin
		self.pin.off()

	def feed(self):
		self.pin.on()
		sleep_ms(20)
		self.pin.off()

