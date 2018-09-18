#!/usr/bin/python
# Process of operations
<<<<<<< HEAD
# Default: reads the sensors every 500ms 

=======
# Default: reads the sensors every 500ms
from datetime import datetime
>>>>>>> 1c7c55ab2365bbbe166a22a5bf0bee383c66b4d7
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import os
import ldr

GPIO.setmode(GPIO.BCM)

<<<<<<< HEAD
# button pins #I think this means the actual pinout...
reset_btn = 1
=======
# button pins
reset_btn = 14
>>>>>>> 1c7c55ab2365bbbe166a22a5bf0bee383c66b4d7
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
	pass

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

	pass

# assign callback functions to falling edge detection on pins
GPIO.add_event_detect(reset_btn, GPIO.FALLING, callback=reset, bouncetime=200)
GPIO.add_event_detect(freq_btn, GPIO.FALLING, callback=freq, bouncetime=200)
GPIO.add_event_detect(stop_btn, GPIO.FALLING, callback=stop, bouncetime=200)
GPIO.add_event_detect(display_btn, GPIO.FALLING, callback=display, bouncetime=200)




# Main loop
try:
	# initialise variables
	frequency = 0.5     # sample rate s
	# global variable
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
	
	values = [0] * 8    # ADC reading
	clock_start = time.time()
	sampling_on = True
	history = [0]*5

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
		lightPercentage = ldr.Read( values[0] )

		clock_time = time.ctime()[10:19]
		clock_current = time.time()
		timer = clock_current - clock_start
		if(sampling_on):
			timer = float('%.2f'%timer)
			timer_clock = datetime.utcfromtimestamp(timer)
			timer_clock = timer_clock.strftime("%H:%M:%S.%f")[:11]
			print('{:10} {:10} {:>10} {:>10} {:>10}'.format(clock_time, timer_clock, potV, 'Temp', lightPercentage))

except KeyboardInterrupt:
	GPIO.cleanup()

GPIO.cleanup()
