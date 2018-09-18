#!/usr/bin/python
# Process of operations
# Default: reads the sensors every 500ms 

import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import os
import ldr

GPIO.setmode(GPIO.BCM)

# button pins #I think this means the actual pinout...
reset_btn = 1
freq_btn = 2
stop_btn = 3
display_btn = 4

# ADC pin definition
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8



GPIO.setup(reset_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(freq_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(display_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# initialize ADC
mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)

# Call-back functions
def reset(reset_btn):
	# Resets the timer and cleans the console
	pass

def freq(freq_btn):
	# changes the sampling rate between: 500ms, 1s, 2s

	pass

def stop(stop_btn):
	# Stops or starts the reading (sampling) of the sensors
	# does not affect the timer
	pass

def display(display_btn):
	# Displays the first 5 readings since the sop switch was pressed

	pass

# assign callback functions to falling edge detection on pins
GPIO.add_event_detect(reset_btn, GPIO.FALLING, callback=reset, bouncetime=200)
GPIO.add_event_detect(freq_btn, GPIO.FALLING, callback=reset, bouncetime=200)
GPIO.add_event_detect(stop_btn, GPIO.FALLING, callback=reset, bouncetime=200)
GPIO.add_event_detect(display_btn, GPIO.FALLING, callback=reset, bouncetime=200)




# Main loop
try:
	# initialise variables
	frequency = 0.5     # sample rate s
	# global variable
	values = [0] * 8
	ldr = LDR()

	print("Calibrating LDR...")
	
	print("Set lowest lighting bound for LDR")
	print("Ready? [y]")
	key = input()
	while (key != 'y'):
		key = input()
	ldr.calibrateMin( mcp.read_adc(0) )

	print("Set upper lighting bound for LDR")
	print("Ready? [y]")
	key = input()
	while (key != 'y'):
		key = input()
	ldr.calibrateMax( mcp.read_adc(0) )
	
	while True:
		for i in range(8):
			values[i] = mcp.read_adc(i)
		# delay for a sample rate frequency
		time.sleep(frequency)
		print(values)

	pass
except KeyboardInterrupt:
	GPIO.cleanup()

GPIO.cleanup()
