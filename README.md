# EEPROMProgrammer
EEPROM Programmer Written in Python and C for Raspberry Pi 3

Inspired by Ben Eater's 6502 breadboard computer kit, this EEPROM programmer tool kit designed for the AT28C256 EEPROM.

While experimenting with writing this script in Python, I found the write timing to be imprecise. Thus, for reading EEPROM contents, the python script is fine, but when writing, the c script should be used.

### Hardware setup
I recomment a Raspberry Pi breakout board like [this one](https://www.amazon.com/Kuman-Expansion-Raspberry-Solderless-Breadboard/dp/B074DSMPYD).

`$ gpio readall` will show you the pinouts for different pin numbering systems. We will use the BCM/wPi numbering. Connections should be as followed (following the BCM pin numbering):

| EEPROM | BCM | wPi |
|--------|-----|-----|
| A0     | 10  | 12  |
| A1     | 9   | 13  |
| A2     | 11  | 14  |
| A3     | 25  | 6   |
| A4     | 8   | 10  |
| A5     | 7   | 11  |
| A6     | 5   | 21  |
| A7     | 6   | 22  |
| A8     | 12  | 26  |
| A9     | 13  | 23  |
| A10    | 19  | 24  |
| A11    | 26  | 25  |
| A12    | 16  | 27  |
| A13    | 20  | 28  |
| A14    | 21  | 29  |
| D0     | 14  | 15  |
| D1     | 15  | 16  |
| D2     | 18  | 1   |
| D3     | 17  | 0   |
| D4     | 27  | 2   |
| D5     | 22  | 3   |
| D6     | 23  | 4   |
| D7     | 24  | 5   |


### Usage

For reading `$ python3 programmer.py`

To compile the c file, run `$ gcc -Wall -o programmer programmer.c -lwiringPi`

For writing a binary file `$ ./programmer <filename>`

For creating binary file edit `makerom.py`, then run `$ python3 makerom.py`
