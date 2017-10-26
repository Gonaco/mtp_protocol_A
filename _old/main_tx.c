#include <stdlib.h>
#include <stdio.h>

#include "RF24.h"


const uint64_t pipes[2] = { 0xF0F0F0F0E1LL, 0xF0F0F0F0D2LL };
void setup(void)
{
	rf24_init_radio("/dev/spidev0.0", 8000000, 25); 
	rf24_setRetries(15,15);
	rf24_setChannel(0x4c);
	rf24_setPALevel(RF24_PA_MAX);
   	rf24_openWritingPipe(pipes[0]);
	rf24_openReadingPipe(1,pipes[1]);
	rf24_startListening();
}

void main(void){
	begin()
	setAutoAck(false);
	bool syncked= false
	while(not syncked)	
		syncked=sync()
	sendData() //in quickmode if we only want to make ping, only send once
	//after quickmode it will be inside a while and using window
	int acked=0
	openReadingPipe()
	startListening()
	while(acked!=1)
		if acked=2
		//we received a NACK so we should resend
			sendData()
			ack=0 //we want to wait for the next ACK
		else
		//it's 0, se we are still waiting for ACK or NACK
			ack=acked()
	//we recived an ACK
	stopListening()
	//in the final mode is after sending the whole file, so after getting out of the while
	sendAck(0);
	int finished=0
	while(finished!=1)
		finished=acked()
	closeConnection()
}


boolean sync()
	int sync= 0;
    	sendSync()
	openReadingPipe()
    	startListening()
	while (sync=0)
    		sync=acked();
	stopListening()
	//you are only going to receive ack or nothing, never nack
	return true


int acked()
	int acked=0
	if somethingReceived (available()¿?)
        	openPacket()
        	int type=checkType();
		if type=ack
			acked=1
		//in the final one we should also check how many have been acked
		else if type=nack
			acked=2
	return acked


void closeConnection()
