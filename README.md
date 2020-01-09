# EEPROMProgrammer
EEPROM Programmer Written in Python for Raspberry Pi 3

Usage:

For reading `python3 programmer.py`

To compile the c file, run `gcc -Wall -o programmer programmer.c -lwiringPi`

For writing a binary file `./programmer <filename>`

For creating binary file edit `makerom.py`, then run `python3 makerom.py`
