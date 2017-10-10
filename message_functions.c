#include <stdlib.h>
#include <stdio.h>

#include <string.h>

#include "libraries/RF24/src/rf24.h"

bool send(char message){

  bool isSent;
  int length = strlen(message); //Is this enough to know th bytes? Maybe multiply by the sizeof(unsigned char)
  isSent = rf24_write_payload(&message, length); //rf24_write or rf24_write_payload ?

  return isSent;

}



