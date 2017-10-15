
#include "message_functions.h"

bool send(unsigned char frame[]){

  bool is_sent;
  uint8_t length_bytes = strlen(frame)*sizeof(unsigned char); //Shouldn't we use a uintblablabla bigger?
  is_sent = rf24_write_payload(&frame, length_bytes); //rf24_write or rf24_write_payload ?

  return is_sent;

}

void frameAssembly(struct header head, unsigned char message[]){

  unsigned char *frame;
  // int crc = crcCalculation(); 
  
  // frame = head + message concatenation

}

bool sendData(unsigned char message[]){

  struct header dataHead;
  dataHead.signature = A_TEAM;
  // dataHead.id = packetIdCalc(); // Function that follows the number of packets sent and gives you the next one
  dataHead.type = 0b11;
  // dataHead.padding = needsPadding(message);
  

  frame = frameAssembly(dataHead, message);

  return send(frame);

}



// NACHO, ESCRIBE A PARTIR DE ESTA LÍNEA. PARA EVITAR COSAS RARAS EN LA FORMA DE PROCESAR CAMBIOS DE GITHUB


