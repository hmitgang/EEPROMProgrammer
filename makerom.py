rom = bytearray([0xea] * 32768)

with open("rom.bin", "wb") as outfile:
	outfile.write(rom)