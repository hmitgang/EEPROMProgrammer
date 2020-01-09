#include <stdio.h>
#include <wiringPi.h>

#define CE_PIN 8 // 2
#define OE_PIN 9 // 3
#define WE_PIN 7 // 4

void writeByte(int address, uint8_t byte);
void setAddress(int address);

// # [A0, A1,..., A12, A13, A14]
// BCM: char addressPins[] = {10, 9, 11, 25, 8, 7, 5, 6, 12, 13, 19, 26, 16, 20, 21};
uint8_t addressPins[] = {12, 13, 14, 6, 10, 11, 21, 22, 26, 23, 24, 25, 27, 28, 29};

// # [D0, D1, D2, D3, D4, D5, D6, D7]
// BCM: char dataPins[] = {14, 15, 18, 17, 27, 22, 23, 24};
uint8_t dataPins[] = {15, 16, 1, 0, 2, 3, 4, 5};

int main(int argc, char const *argv[])
{
	// Setup
	if(argc != 2) {
		printf("Enter a binary file to write.\n");
		return 1;
	}
	printf("Ensure 5V connected, then hit return.");
	scanf("%c");

	wiringPiSetup();

	pinMode(CE, OUTPUT);
	digitalWrite(CE, HIGH); // Active low	
	pinMode(OE, OUTPUT);
	digitalWrite(OE, HIGH); // Active low
	pinMode(WE, OUTPUT);
	digitalWrite(WE, HIGH); // Active low

	for(uint8_t pin: addressPins){
		pinMode(pin, OUTPUT);
		digitalWrite(pin, LOW);
	}

	for(uint8_t pin: dataPins){
		pinMode(pin, OUTPUT);
	}

	FILE *binFile;
	uint8_t curByte;
	unsigned int address = 0;

	binFile = fopen("rom.bin","rb");
	
	digitalWrite(CE, LOW) // Enable chip

	while(fscanf(binFile, "%c", &curByte)==1){
		printf("0x%04x  0x%02x\n", address, curByte);
		writeByte(address, curByte)
		address++;
	}
	
	fclose(binFile);

	return 0;
}

void writeByte(int address, uint8_t byte){
	setAddress(address);
	for(uint8_t pin: dataPins) {
		digitalWrite(pin, byte & 1);
		byte = byte >> 1
	}

	digitalWrite(WE, LOW);
	delayMicroseconds(1);
	digitalWrite(WE, HIGH);
	delay(10);

}

void setAddress(int address){
	for(uint8_t pin: addressPins){
		digitalWrite(pin, address & 1);
		address = address >> 1
	}
}