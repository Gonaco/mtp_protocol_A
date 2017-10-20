#include "message_functions.h"

int main(){

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
