#include <stdlib.h>
#include <stdio.h>

#include <string.h>

#include "RF24.h"

bool send(char message){

  bool isSent;
  int length = strlen(message);
  isSent = rf24_write_payload(&message, length); //rf24_write or rf24_write_payload ?

  return isSent;

}
