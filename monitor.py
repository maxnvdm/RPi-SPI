
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import os

GPIO.setmode(GPIO.BCM)
# pin definition
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)
# global variable
values = [0]*8
while True:
	for i in range(8):
		values[i] = mcp.read_adc(i)
	# delay for a half second
	time.sleep(0.5)
	print(values)