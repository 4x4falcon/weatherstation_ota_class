from time import sleep_ms

class Watchdog:
	def __init__(self, pin):
		self.pin = pin
		self.pin.off()

	def feed(self):
		self.pin.on()
		sleep_ms(100)
		self.pin.off()
		print ("Watchdog fed")
