#include <stdlib.h>
#include <stdio.h>

#include <string.h>

#include "libraries/RF24/src/rf24.h"

bool send(unsigned char message[]){

  bool is_sent;
  uint8_t length_bytes = strlen(message)*sizeof(unsigned char);
  is_sent = rf24_write_payload(&message, length_bytes); //rf24_write or rf24_write_payload ?

  return is_sent;

}



