# modified from https://www.instructables.com/id/Raspberry-Pi-Python-EEPROM-Programmer/

import RPi.GPIO as GPIO
import sys, time

GPIO.setmode(GPIO.BCM) #Use chip numbering scheme
GPIO.setwarnings(False)


CE = 2
OE = 3
WE = 4
LOW  = 0
HIGH = 1

# Setup CE, OE, and WE
GPIO.setup(CE, GPIO.OUT)
GPIO.setup(OE, GPIO.OUT)
GPIO.setup(WE, GPIO.OUT)


# [A0, A1,..., A12, A13, A14]
addressPins = [10, 9, 11, 25, 8, 7, 5, 6, 12, 13, 19, 26, 16, 20, 21]

# [D0, D1, D2, D3, D4, D5, D6, D7]
dataPins = [14, 15, 18, 17, 27, 22, 23, 24]


#Set the chip in standby mode while setting up the rest GPIO:
GPIO.output(CE, HIGH) #CE - high -- Active LOW
GPIO.output(OE, HIGH) #OE - high -- SHOULD ALWAYS HIGH FOR WRITE
GPIO.output(WE, HIGH) #WE - high


# Set up address pin modes
for pin in addressPins:
	GPIO.setup(pin, GPIO.OUT)


def setAddress(address):
	"""Sets GPIO pins to an address"""
	# Least significant digit first (i.e. A0 is least significant)
	for pin in addressPins:
		GPIO.output(pin, address & 1)
		address = address >> 1
	

def writeByte(address, data):
	"""Writes byte data at address"""
	GPIO.output(OE, HIGH)

	# Set up data pins
	for pin in dataPins:
		GPIO.setup(pin, GPIO.OUT)

	setAddress(address)
	# Least significant digit first (i.e. D0 is least significant)
	for pin in dataPins:
		GPIO.output(pin, data & 1)
		data = data >> 1

	GPIO.output(WE, LOW)
	time.sleep(1e-6)
	GPIO.output(WE, HIGH)
	time.sleep(.001)

def readByte(address):
	"""Read byte at an address
	Returns the data at that address as int"""

	GPIO.output(OE, LOW)
	# Set up data pins
	for pin in dataPins:
		GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

	data = 0
	# Least significant digit first (i.e. D0 is least significant)
	for pin in dataPins[::-1]:
		data = (data << 1) + GPIO.input(pin)

	GPIO.output(OE, HIGH)
	return data


def progressbar(it, prefix="", size=60, file=sys.stdout):
	"""Progress bar used as iterable"""
	
	count = len(it)
	def show(j):
		x = int(size*j/count)
		file.write("%s[%s%s] 0x%04x/0x%04x\r" % (prefix, "#"*x, "."*(size-x), j, count))
		file.flush()        
	show(0)
	for i, item in enumerate(it):
		yield item
		show(i+1)
	file.write("\n")
	file.flush()

if __name__=="__main__":
	if len(sys.argv) == 2:
		print("Writing",sys.argv[1], "to EEPROM...")
		with open(sys.argv[1], "rb") as inFile:
			for address, byte in enumerate(progressbar(inFile.read(), "Writing: ", 40)):
				# print("Address: "+"{0:#0{1}x}".format(address,6), "Data: "+"{0:#0{1}x}".format(byte,2))
				writeByte(address, byte)
		print("Complete!")
	else:
		readSize = int(input("Input read size (32768): "))
		for base in range(0, readSize, 16):
			data = []
			for offset in range(16):
				data += [hex(readByte(base + offset))]

			print("Addr 0x" + hex(base) + ": " + " ".join(data))


GPIO.cleanup()

