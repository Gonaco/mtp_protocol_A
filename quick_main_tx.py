#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import message_functions as m




pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]] #addresses for TX/RX channels

radio2 = NRF24(GPIO, spidev.SpiDev()) 
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(1, 27) # Set spi-cs pin0, and rf24-CE pin 17
radio2.begin(0, 17)

time.sleep(1)
radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(0x65)
radio2.setRetries(15,15)
radio2.setPayloadSize(32)
radio2.setChannel(0x60)

radio2.setDataRate(NRF24.BR_2MBPS)
radio2.setPALevel(NRF24.PA_MAX)
radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(False)
radio.enableDynamicPayloads() # radio.setPayloadSize(32) for setting a fixed payload
radio.enableAckPayload()
radio2.setAutoAck(False)
radio2.enableDynamicPayloads()
radio2.enableAckPayload()

radio.openWritingPipe(pipes[1])
radio2.openReadingPipe(1, pipes[0])
radio.printDetails()

radio2.startListening();

paysize = 30 # size of payload we send at once
timeout = time.time() + 0.1
eof_delimiter = "ThIs Is EnD oF FiLe..........."
    
##################DEBUG CODE BELOW############################
run = True
repeat = False
while run:
    infile = open("tx_file.txt", "r")
    data = infile.read()
    infile.close()
    data_id=1
    for i in range(0, len(data), paysize):
        if (i+paysize) < len(data):
            buf = data[i:i+paysize]
            print("sending full packet")
        else:
            print("sending partial packet")
            buf = data[i:]
            run = False
        #frame=m.Frame(data_id, 0, buf)
        print("We'll try sending")
        #frame.send(radio)
        radio.write(buf)
        print ("Sent:"),
        #print (frame)
        # did it return with a payload?
        num=0
        pipe = [1]
        repeat = False
        while not radio2.available(pipe) and num < 100:
            time.sleep(10000/1000000.0)
            num = num+1

        if num == 500:
            i = i - 1 # we'll repeat the packet

        pl_buffer=[]
        radio2.read(pl_buffer, radio2.getDynamicPayloadSize())
        print ("Received back:"),
        print (pl_buffer)
        #data_id += 1

        if run == False:
            print ("Sending final packet")
            radio.write(eof_delimiter)

        time.sleep(50) # wait a bit for processing


print("Done sending the file! Exiting!")


