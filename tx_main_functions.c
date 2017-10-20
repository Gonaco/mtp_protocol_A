#include "tx_main_functions.h"

void setupTx()
{
	RF24_begin(void);
	RF24_setRetries(15,15);
	RF24_setChannel(0x4c);
	RF24_setPALevel(RF24_PA_MAX);
   	RF24_openWritingPipe(pipes[0]);
	RF24_openReadingPipe(1,pipes[1]);
	// en el codigo de ejemplo aparece pero no se si es necesario si se que lo primero que voy a hacer es enviar igual para saver details
	RF24_startListening();
	RF24_printDetails();
	RF24_stopListening();
}
