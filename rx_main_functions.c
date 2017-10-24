#include "rx_main_functions.h"

const uint8_t pipes[][6] = {"1Node","2Node"};

void setupRx()
{
	RF24_init2(); /* Por completar */
	RF24_begin();
	RF24_setRetries(15,15);
	RF24_setChannel(0x4c);
	RF24_setPALevel(RF24_PA_MAX);
	RF24_openReadingPipe(1,pipes[1]);
	RF24_startListening();
	RF24_printDetails();
}

