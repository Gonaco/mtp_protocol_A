#include "message_functions.h"

int main(){

  rf24_init_radio("/dev/spidev0.0", 8000000, 25);
  rf24_setRetries(15,15);
  rf24_setChannel(0x4c);
  rf24_setPALevel(RF24_PA_MAX);
  /* rf24_openReadingPipe(1,pipes[1]); */
  // en el codigo de ejemplo aparece pero no se si es necesario si se que lo primero que voy a hacer es enviar igual para saver details
  rf24_startListening();
  rf24_printDetails();
  rf24_stopListening();

  unsigned char text[] = "Message from A-Team";

  printf("\n%s\n", text);

  bool a = send(text);

  if(a){

    printf("works\n");

      }
  else {

    printf("what?\n");

      }

  return 0;
  
}
