#include "message_functions.h"

bool send(unsigned char frame[]){

  bool is_sent;
  uint8_t length_bytes = strlen(frame)*sizeof(unsigned char); //Shouldn't we use a uintblablabla bigger?
  is_sent = RF24_write(&frame, length_bytes); //rf24_write or rf24_write_payload ?

  return is_sent;

}

int header2string(struct header head, char *string_header){

}


int frame2string(struct frame fr, char *string_frame){

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

rf24_writeAckPayload(	uint8_t pipe, const void * buf, uint8_t len)	
  //pipe:	Which pipe# (typically 1-5) will get this response.
  //buf:	Pointer to data that is sent
  //len:	Length of the data to send, up to 32 bytes max.
 
/* In case that the function given in the libraries won't work:
bool sendAck(identification){
  struct header ackHead;
  ackHead.signature = A_TEAM;
  ackHead.id = identification; //When we call the function sendACK, we have to tell it which ACK we're sending, no?
  ackHead.type = 0b01; //Let's suppose that 01 is the code for ACKs
  ackHead.padding = 0b0; //A ACK packet will never have padding
  
  ack = frameAssembly(ackHead, 0b0); //Should we send ACKs whith empty payload? How do we do so?

  return send(ack);

}
*/

bool sendNack(unsigned char identification, double nacked){
  struct header nackHead;
  nackHead.signature = A_TEAM;
  nackHead.id = identification; //When we call the function sendNack, we have to tell it which NACK we're sending, no?
  nackHead.type = 0b10; //Let's suppose that 10 is the code for NACKs
  nackHead.padding = 0b0; //A NACK packet will never have padding
  //bin_nacked = ; Im supposing that nacked is a vector and we have to pass it to binary. How do we do so?
  nack = frameAssembly(nackHead, bin_nacked); //

  return send(nack);

}

bool sendSync(){
  struct header syncHead;
  syncHead.signature = A_TEAM;
  syncHead.id = 0b0; //SYNC packets doesn't have ID
  syncHead.type = 0b00; //Let's suppose that 00 is the code for SYNCs
  synckHead.padding = 0b0; //A SYNC packet will never have padding
  
  sync = frameAssembly(syncHead, 0b0); //SYNCs doesn't have any payload. Is it ok?

  return send(sync);

}
