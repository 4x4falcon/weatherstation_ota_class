rf = 0
ws = 0
ntpset = 0
bright = 0
esp32=True

# toggle function
def toggle(p):
        p.value(not p.value())



# get battery voltage function

# formula is:
# ADC.read()/4096 * maximum voltage * ( resistor calculated / resistor actual)
# resistor calculated is from https://ohmslawcalculator.com/voltage-divider-calculator
# resistor actual is actual resistance used. Usually from preferred values.

def getBatteryVoltage(batteryvoltage):
	global esp32
	from machine import Pin, ADC

# values of resistors in external voltage divider
#	R1 = 96.0
#	R2 = 34.1

	if (esp32):
#ESP 32
		adc = ADC(Pin(36))
	else:
#ESP 8266
		adc = ADC(0)

	raw = adc.read()

	if (esp32):
#ESP 32
		return raw/3520 * batteryvoltage
	else:
#ESP 8266
		return raw/1024 * batteryvoltage



# isr for rainfall counter
# rainfall interrupt callback
def rainfall_cb(d):
	global rf
	rf += 1
	print("Rainfall toggled", rf)


# isr for wind speed counter
# rainfall interrupt callback
def windspeed_cb(d):
	global ws
	ws += 1
	print("Windspeed toggled", ws)


# read the current wind direction
# return wind direction in degrees

def getWinddir():
	global esp32
	from machine import Pin, ADC

	winddir = 0

	if (esp32):
#ESP 32
		adc = ADC(Pin(35))
		adc.atten(ADC.ATTN_11DB)
	else:
#ESP 8266
		adc = ADC(0)

	raw = adc.read()

# may need averaging of 3 or more readings

#					Raw Value	Raw Value			Range			Range
#	Dir		Deg		calculated	actual		Ohm		calculated		acutual

#	N		0		3143		2830		33k		2976 - 3226		2667 - 2928
#	NNE		22.5		1623		1378		6.57k		1300 - 1734		1149 - 1484
#	NE		45		1845		1590		8.2k		1734 - 2121		1484 - 1812
#	ENE		67.5		335		148		891		300 - 353		114 - 131
#	E		90		372		182		1k		353 - 444		131 - 244
#	ESE		112.5		263		80		688		< 300			< 114
#	SE		135		738		532		2.2k		622 - 858		419 - 645
#	SSE		157.5		506		306  ???	1.41k		444 - 622		244 - 419
#	S		180		1148		920		3.9k		1063 - 1300		839 - 1149
#	SSW		202.5		978		758		3.14k		858 - 1063		645 - 839
#	SW		225		2520		2228		16k		2448 - 2665		2171 - 2366
#	WSW		247.5		2397		2114		14.12k		2121 - 2448		1812 - 2171
#	W		270		3780		3734		120k		> 3664			> 3380
#	WNW		292.5		3309		3026		42.12k		3226 - 3428		2928 - 3191
#	NW		315		3548		3356		64.9k		3428 - 3664		3191 - 3380
#	NNW		337.5		2810		2503		21.88k		2665 - 2976		2366 - 2667

#	Raw value is for esp32
#	Use 10k resistor to 3.3V
#	these are calulated values need to confirm by experiment
#	ohm values are from Fine Offset DS-15901 data sheet

	print("Raw: ", raw)

	if ( raw < 114 ):
		winddir = 112.5
	if ( raw >= 114 ) and ( raw < 131 ):
		winddir = 67.5
	if ( raw >= 131 ) and ( raw < 244 ):
		winddir = 90.0
	if ( raw >= 244 ) and ( raw < 419 ):
		winddir = 157.5
	if ( raw >= 419 ) and ( raw < 645 ):
		winddir = 135.0
	if ( raw >= 645 ) and ( raw < 839 ):
		winddir = 202.5
	if ( raw >= 839 ) and ( raw < 1149 ):
		winddir = 180.0
	if ( raw >= 1149 ) and ( raw < 1484 ):
		winddir = 22.5
	if ( raw >= 1484 ) and ( raw < 1812 ):
		winddir = 45.0
	if ( raw >= 1812 ) and ( raw < 2171 ):
		winddir = 247.5
	if ( raw >= 2171 ) and ( raw < 2366 ):
		winddir = 225.0
	if ( raw >= 2366 ) and ( raw < 2667 ):
		winddir = 337.5
	if ( raw >= 2667 ) and ( raw < 2928 ):
		winddir = 0.0
	if ( raw >= 2928 ) and ( raw < 3191 ):
		winddir = 292.5
	if ( raw >= 3191 ) and ( raw < 3380 ):
		winddir = 315.0
	if ( raw >= 3380 ):
		winddir = 270.0


	return winddir

# get rainfall counts and reset to zero if true
def getRainfall(zero=True):
	global rf
	t = rf
	if (zero):
		rf = 0
	return t

# get windspeed counts and reset to zero if true
def getWindspeed(zero=True):
	global ws
	t = ws
	if (zero):
		ws = 0
	return t


# check if rtc needs updating from ntp after 30 minutes (1800 seconds)
def resetntp(t):
	global ntpset
	if (t > ntpset + 1800):
		ntpset = t
		return True
	return False


# connect wifi
def do_connect(SSID, Pass):
	import network
	wlan = network.WLAN(network.STA_IF)
	wlan.active(True)
	if not wlan.isconnected():
		print('connecting to network...')
		wlan.connect(SSID, Pass)
		while not wlan.isconnected():
			pass
	print('network config:', wlan.ifconfig())

# reconnect wifi
def reconnect():
	return True
