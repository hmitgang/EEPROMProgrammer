rom = bytearray([0xea] * 200)

rom[0] = 0xaa

rom[-10] = 0x55

with open("rom.bin", "wb") as outfile:
	outfile.write(rom)