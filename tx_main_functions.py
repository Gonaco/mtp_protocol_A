#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev



pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]] #addresses for TX/RX channels

radio2 = NRF24(GPIO, spidev.SpiDev()) 
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(1, 27) # Set spi-cs pin0, and rf24-CE pin 17
radio2.begin(0, 17)

time.sleep(1)
radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(0x60)
radio2.setRetries(15,15)
radio2.setPayloadSize(32)
radio2.setChannel(0x60)

radio2.setDataRate(NRF24.BR_2MBPS)
radio2.setPALevel(NRF24.PA_MAX)
radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
radio.enableDynamicPayloads() # radio.setPayloadSize(32) for setting a fixed payload
radio.enableAckPayload()
radio2.setAutoAck(True)
radio2.enableDynamicPayloads()
radio2.enableAckPayload()

radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])
radio.printDetails()

paysize = 30 # size of payload we send at once

##################DEBUG CODE BELOW############################
def main():
    run = True

    while run:
        infile = open("tx_file.txt", "r")
        data = infile.read()
        infile.close()
        data_id=1
        if  synchronized():
            for i in range(0, len(data), paysize):
                if (i+paysize) < len(data):
                    buf = data[i:i+paysize]
                else:
                    buf = data[i:]
                    run = False
                frame=Frame(data_id, 0, buf)
                # radio.write(frame)
                frame.send(radio)
                print ("Sent:"),
                print (frame)
                # did it return with a payload?
                if radio.available():
                    pl_buffer=[]
                    radio.read(pl_buffer, radio.getPayloadSize())
                    print ("Received back:"),
                    print (pl_buffer)
                else:
                    print ("Received: Ack only, no payload")
                data_id += 1

    fin_connection()
    return 0

def synchronized():
    done=false
    sync=Header(97, SYNC, 1)
    radio.write(sync)
    radio.startListening()
    if radio.available():
        radio.read(buffer, radio.getPayloadSize())
        print("Sync done")
        done=true
    return done;

def fin_connection():
    ack=ACK(0, 0)
    radio.write(ack)
    radio.startListening()
    if radio.available():
        radio.read(buffer, radio.getPayloadSize())
        print("Done sending the file! Exiting!")

    return;
