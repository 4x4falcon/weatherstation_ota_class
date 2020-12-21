rf = 0
ws = 0
ntpset = 0
bright = 0
esp32=True

import network
wlan = network.WLAN(network.STA_IF)


# toggle function
def toggle(p):
        p.value(not p.value())


# select esp32 or esp8266
def setEsp32():
	global esp32
	from os import uname
	if (uname().sysname == 'esp8266'):
	       esp32 = False
	       print ("found esp8266")
	return esp32



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
# when using 100k resistors for R1 and R2 then need the adc.atten(ADC.ATTN_11DB) otherwise comment it out

	if (esp32):
#ESP 32
		adc = ADC(Pin(36))
		adc.atten(ADC.ATTN_11DB)


	else:
#ESP 8266
		adc = ADC(0)

	raw = adc.read()

	print ("bv: ", raw)

	if (esp32):
#ESP 32
# when using 100k resistors for R1 and R2 then use 2220 as divisor
#		return raw/3520 * batteryvoltage
		return raw/2220 * batteryvoltage
	else:
#ESP 8266
		return raw/1024 * batteryvoltage



# isr for rainfall counter
# rainfall interrupt callback
def rainfall_cb(d):
	global rf
	rf += 1
#	print("rf ", rf)


# isr for wind speed counter
# rainfall interrupt callback
def windspeed_cb(d):
	global ws
	ws += 1
#	print("ws ", ws)

def interrupt_cb(d):
	global ws
	global rf

	if (d == "r"):
		rf += 1
#		print("rf: ", rf)
	elif (d == "w"):
		ws += 1
#		print("ws: ", ws)


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

#					Raw Value	Raw Value	Raw Value			Range			Range		Range
#	Dir		Deg		calculated	actual		actual		Ohm		calculated		actual		actual
#							Strathdickie	Riverbank						Strathdickie	Riverbank

#	N		0		3143		2830		2894		33k		2976 - 3226		2667 - 2928	2727 - 3000
#	NNE		22.5		1623		1378		1414		6.57k		1300 - 1734		1149 - 1484	1174 - 1522
#	NE		45		1845		1590		1630		8.2k		1734 - 2121		1484 - 1812	1522 - 1857
#	ENE		67.5		335		148		161		891		300 - 353		114 - 131	126 - 179
#	E		90		372		182		199		1k		353 - 444		131 - 244	179 - 262
#	ESE		112.5		263		80		91		688		< 300			< 114		< 126
#	SE		135		738		532		550		2.2k		622 - 858		419 - 645	438 - 667
#	SSE		157.5		506		306  ???	326		1.41k		444 - 622		244 - 419	262 - 438
#	S		180		1148		920		951		3.9k		1063 - 1300		839 - 1149	868 - 1174
#	SSW		202.5		978		758		785		3.14k		858 - 1063		645 - 839	667 - 868
#	SW		225		2520		2228		2277		16k		2448 - 2665		2171 - 2366	2221 - 2419
#	WSW		247.5		2397		2114		2165		14.12k		2121 - 2448		1812 - 2171	1857 - 2221
#	W		270		3780		3734		3822		120k		> 3664			> 3380		> 3628
#	WNW		292.5		3309		3026		3096		42.12k		3226 - 3428		2928 - 3191	3000 - 3265
#	NW		315		3548		3356		3434		64.9k		3428 - 3664		3191 - 3380	3265 - 3628
#	NNW		337.5		2810		2503		2560		21.88k		2665 - 2976		2366 - 2667	2419 - 2727

#	Raw value is for esp32
#	Use 10k resistor to 3.3V
#	these are calulated values need to confirm by experiment
#	ohm values are from Fine Offset DS-15901 data sheet

	print("Raw: ", raw)

	if ( raw < 126 ):
		winddir = 112.5
	if ( raw >= 126 ) and ( raw < 179 ):
		winddir = 67.5
	if ( raw >= 179 ) and ( raw < 262 ):
		winddir = 90.0
	if ( raw >= 262 ) and ( raw < 438 ):
		winddir = 157.5
	if ( raw >= 438 ) and ( raw < 667 ):
		winddir = 135.0
	if ( raw >= 667 ) and ( raw < 868 ):
		winddir = 202.5
	if ( raw >= 868 ) and ( raw < 1174 ):
		winddir = 180.0
	if ( raw >= 1174 ) and ( raw < 1522 ):
		winddir = 22.5
	if ( raw >= 1522 ) and ( raw < 1857 ):
		winddir = 45.0
	if ( raw >= 1857 ) and ( raw < 2221 ):
		winddir = 247.5
	if ( raw >= 2221 ) and ( raw < 2419 ):
		winddir = 225.0
	if ( raw >= 2419 ) and ( raw < 2727 ):
		winddir = 337.5
	if ( raw >= 2727 ) and ( raw < 3000 ):
		winddir = 0.0
	if ( raw >= 3000 ) and ( raw < 3265 ):
		winddir = 292.5
	if ( raw >= 3265 ) and ( raw < 3628 ):
		winddir = 315.0
	if ( raw >= 3628 ):
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
#	print("t: ", t)
#	print("ntpset: ", ntpset)
	if (t > ntpset + 1800):
		ntpset = t
		return True
	return False

# set ntpset
def setntpset(t):
	global ntpset
	ntpset = t

# get current ntpset
def getntpset():
	global ntpset
	return ntpset


# Load Wifi Configuration from JSON file.
#def load_wifi_config():
#        wifi_config = None
#        config_filename = '/config/wifi_cfg.json'
#        try:
#                with open(config_filename) as json_config_file:
#	                wifi_config = json.load(json_config_file)
#        except Exception:
#		print('No file')
#                pass
#        return wifi_config


# connect wifi
def do_connect(SSID, Pass, Host):
#	import network
	global wlan
	print("connecting to: ", SSID)
#	wlan = network.WLAN(network.STA_IF)
	wlan.active(True)
	if not wlan.isconnected():
		print('connecting to network...')
		wlan.connect(SSID, Pass)
		while not wlan.isconnected():
			pass
	wlan.config(dhcp_hostname=Host)
	print('network config:', wlan.ifconfig())

# reconnect wifi
def reconnect():
	return True

