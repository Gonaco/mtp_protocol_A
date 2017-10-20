#include "tx_main_functions.h"

void setupTx()
{
	rf24_init_radio("/dev/spidev0.0", 8000000, 25); 
	rf24_setRetries(15,15);
	rf24_setChannel(0x4c);
	rf24_setPALevel(RF24_PA_MAX);
   	rf24_openWritingPipe(pipes[0]);
	rf24_openReadingPipe(1,pipes[1]);
	// en el codigo de ejemplo aparece pero no se si es necesario si se que lo primero que voy a hacer es enviar igual para saver details
	rf24_startListening();
	rf24_printDetails();
	rf24_stopListening();
}
