# modified from https://www.instructables.com/id/Raspberry-Pi-Python-EEPROM-Programmer/

import RPi.GPIO as GPIO
import sys, time

# Global constants
CE = 2
OE = 3
WE = 4
LOW  = 0
HIGH = 1

# [A0, A1,..., A12, A13, A14]
addressPins = [10, 9, 11, 25, 8, 7, 5, 6, 12, 13, 19, 26, 16, 20, 21]

# [D0, D1, D2, D3, D4, D5, D6, D7]
dataPins = [14, 15, 18, 17, 27, 22, 23, 24]


def setup():
	"""Setup GPIO modes"""

	#Use chip numbering scheme
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	# Setup CE, OE, and WE
	GPIO.setup(CE, GPIO.OUT, initial=HIGH)
	GPIO.setup(OE, GPIO.OUT, initial=HIGH)
	GPIO.setup(WE, GPIO.OUT, initial=HIGH)

	#Set the chip in standby mode while setting up the rest GPIO:
	GPIO.output(CE, HIGH) #CE - high -- Active LOW
	GPIO.output(OE, HIGH) #OE - high -- Active LOW -- SHOULD ALWAYS HIGH FOR WRITE
	GPIO.output(WE, HIGH) #WE - high -- Active LOW

	# Set all address pins to output
	GPIO.setup(addressPins, GPIO.OUT)
	print("Setup. Ready to begin.")
	GPIO.output(CE, LOW)


def cleanup():
	"""Cleanup after use."""
	GPIO.cleanup()
	print("Cleaned up. Ready to end.")


def setAddress(address):
	"""Sets GPIO pins to an address
	-- Address"""

	# Least significant digit first (i.e. A0 is least significant)
	for pin in addressPins:
		GPIO.output(pin, address & 1) # Get least significant bit
		address = address >> 1 # Shift right to get next least significant bit
	

def writeByte(address, data):
	"""Writes byte data at address
	-- Address
	-- Data"""

	# Ensure output is disabled
	GPIO.output(OE, HIGH)

	# Set up data pins for output since Pi is writing
	GPIO.setup(dataPins, GPIO.OUT)

	setAddress(address)

	# Least significant digit first (i.e. D0 is least significant)
	for pin in dataPins:
		GPIO.output(pin, data & 1) # Get least significant bit
		data = data >> 1 # Shift right to get next least significant bit

	# Pulse WE low to latch data to address:
	# RPi.GPIO direct toggle (with no delay between) results in pulse usual pulse
	# of 3-5 Microseconds sometimes up to 128 Microseconds albeit rare.
	GPIO.output(WE, LOW)
	# time.sleep(1e-6)
	GPIO.output(WE, HIGH)
	time.sleep(.001)


def readByte(address):
	"""Read byte at an address
	Returns the data at that address as int
	-- Address"""

	# Ready chip for output
	GPIO.output(OE, LOW)
	
	# Set up data pins
	GPIO.setup(dataPins, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

	setAddress(address)

	data = 0
	# Most significant digit first as dataPins is reversed
	for pin in dataPins[::-1]:
		# Shift current data left and add next most significant bit
		data = (data << 1) + GPIO.input(pin)

	# Disable further EEPROM output 
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
	# Initialize the GPIO
	setup()

	if len(sys.argv) == 2: # If file to write is specified
		print("Writing", sys.argv[1], "to EEPROM...")

		with open(sys.argv[1], "rb") as inFile:
			for address, byte in enumerate(progressbar(inFile.read(), "Writing: ", 40)):
				writeByte(address, byte)

		print("Complete!")

	else:
		print("Reading from EEPROM! Ensure power supply is 3.3V and NOT 5V as that will fry the Pi!")
		readSize = input("Input read size decimal or hex 0x00 (default 32768): ")
		fileName = input("Input file name (leave blank for None): ")

		if 'x' in readSize: # If hexidecimal
			readSize = int(readSize, 16)
		elif readSize: # If Decimal
			readSize = int(readSize)
		else: # If blank
			readSize = 32768

		if fileName:
			outputFile = open(fileName, 'wb')
		
		for base in range(0, readSize, 16): # Read 16 bytes at a time
			data = []
			for offset in range(16): # Get individual bytes with offset
				data += [readByte(base + offset)]

			if fileName:
				outputFile.write(bytes(data)) # Write to file

			print("Addr " + hex(base) + ": " + " ".join([ hex(byte) for byte in data ])) # Write to console

		if fileName:
			outputFile.close()

	cleanup() # Cleanup GPIO after use
