#!/usr/bin/python
# Process of operations
# Default: reads the sensors every 500ms
from datetime import datetime
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import os
import ldr
import collections

GPIO.setmode(GPIO.BCM)

# button pins
reset_btn = 14
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
	global clock_start
	clock_start = time.time()
	clear = os.system('clear')

def freq(freq_btn):
	# changes the sampling rate between: 500ms, 1s, 2s
	global frequency
	if frequency==0.5:
		frequency=1
	elif frequency==1:
		frequency=2
	elif frequency==2:
		frequency=0.5
	print("Frequency changed to: "+str(frequency)+"s")

def stop(stop_btn):
	# Stops or starts the reading (sampling) of the sensors
	# does not affect the timer
	global sampling_on
	if sampling_on==False:
		sampling_on = True
		print("Start sampling")
	else:
		sampling_on = False
		print("Stop sampling")

def display(display_btn):
	# Displays the first 5 readings since the sop switch was pressed
	global history
	for reading in history:
		print(reading)


# assign callback functions to falling edge detection on pins
GPIO.add_event_detect(reset_btn, GPIO.FALLING, callback=reset, bouncetime=200)
GPIO.add_event_detect(freq_btn, GPIO.FALLING, callback=freq, bouncetime=200)
GPIO.add_event_detect(stop_btn, GPIO.FALLING, callback=stop, bouncetime=200)
GPIO.add_event_detect(display_btn, GPIO.FALLING, callback=display, bouncetime=200)

def toDegrees(voltage):
    m = 100
    c = -50
    return m*voltage + c


# Main loop
try:
	# initialise variables
	frequency = 0.5     # sample rate s
	history = collections.deque("" ,5)
	# global variable
	ldr = ldr.LDR()

	print("Calibrating LDR...")
	
	print("Set lowest lighting bound for LDR")
	print("Ready? [y]")
	key = ""
	while (key != 'y'):
		key = raw_input()
	t0 = mcp.read_adc(0)
	ldr.calibrateMin(t0)

	print("Set upper lighting bound for LDR")
	print("Ready? [y]")
	key = ""
	while (key != 'y'):
		key = raw_input()
	t1 = mcp.read_adc(0)
	ldr.calibrateMax(t1)
	
	values = [0] * 8    # ADC reading
	clock_start = time.time()
	sampling_on = True

	print('{:10} {:10} {:>9} {:>10} {:>10}'.format(' Time', 'Timer', 'Pot', 'Temp', 'Light'))
	while True:
		for i in range(8):
			values[i] = mcp.read_adc(i)
		# delay for a sample rate frequency
		time.sleep(frequency)

		# Pot voltage
		potV = values[1]*(3.3/1024)
		potV = ('%.1f'%potV)+" V"

		#Read LDR value
		lightPercentage = round(ldr.read( values[0] )*100, 0)

		#Temp voltage
		tempVoltage = values[2] * (3.3/1024)

		# Get the temperature in degrees
		tempValue = round(toDegrees(tempVoltage), 2)


		clock_time = time.ctime()[10:19]
		clock_current = time.time()
		timer = clock_current - clock_start
		if(sampling_on):
			timer = float('%.2f'%timer)
			timer_clock = datetime.utcfromtimestamp(timer)
			timer_clock = timer_clock.strftime("%H:%M:%S.%f")[:11]
			readings = [clock_time, timer_clock, potV, tempValue, lightPercentage]
			history.append(readings)
			print('{:10} {:10} {:>10} {:>10} {:>5}'.format(clock_time, timer_clock, potV, tempValue, lightPercentage))

except KeyboardInterrupt:
	GPIO.cleanup()

GPIO.cleanup()
