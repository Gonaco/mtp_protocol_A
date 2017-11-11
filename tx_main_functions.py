#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import message_functions as m


def setup():

    pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]] #addresses for TX/RX channels

    radio2 = NRF24(GPIO, spidev.SpiDev())
    radio = NRF24(GPIO, spidev.SpiDev())
    radio.begin(1, 27) # Set spi-cs pin1, and rf24-CE pin 27
    radio2.begin(0, 17) # Set spi-cs pin0, and rf24-CE pin 17

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

    radio.setAutoAck(False)
    radio.enableDynamicPayloads() # radio.setPayloadSize(32) for setting a fixed payload
    radio.enableAckPayload()
    radio2.setAutoAck(False)
    radio2.enableDynamicPayloads()
    radio2.enableAckPayload()

    radio.openWritingPipe(pipes[1])
    radio.openReadingPipe(1, pipes[0])
    radio.printDetails()

    timeout = time.time() + 0.1
    return radio, radio2
    
##################DEBUG CODE BELOW############################
def transmit(radio, radio2, file):
    run = True
    paysize=27 #may change
    repeat=False
    window_id=1
    window_size=10 #may change
    last_sent=0
    data=file.read()
    frame_list=build_list()
    while run:
        radio.write(frame)
        print("We'll try sending")
        frame.send(radio)
        print ("Sent:"),
        print (frame)
        # did it return with a payload?
        if radio.available():
            pl_buffer=[]
            radio.read(pl_buffer, radio.getDynamicPayloadSize())
            print ("Received back:"),
            print (pl_buffer)
        else:
            if(time.time() + 1/20000>timeout):
                #we resend packet
                frame.send(radio)
                timeout = time.time() + 0.1
            data_id += 1

    end_connection()
    return 0

def synchronized(radio, radio2, pipe):
    done=False
    sync=m.SYNC(0, '')
    # print(sync.extractHeader())
    while not done:
        radio.write(sync.__str__())
        radio2.startListening()
        while not radio2.available(pipe) and num < 400:
            time.sleep(1 / 1000.0)
            num = num + 1
        if num != 400:
            print("we received something before time out")
            rcv_buffer = []
            radio2.read(rcv_buffer, radio2.getDynamicPayloadSize())
            rcv = m.Packet()
            rcv.strMssg2Pckt(rcv_buffer)
            if rcv.getTyp()==1:
                if rcv.getID==0:
                    done=True
    return done


def end_connection():
    ack=m.ACK(0, 0) #for ending connection we send ACK with ID 0
    ack.send(radio)
    radio.startListening()
    if radio.available():
        radio.read(buffer, radio.getPayloadSize())
    print("Done sending the file! Exiting!")

    return;
def build_list(data, paysize):
    data_id = 1
    frame_list = []
    for i in range(0, len(data), paysize):
        if (i + paysize) < len(data):
            buf = data[i:i + paysize]
            frame = m.Frame(data_id, 0, buf)
            i=+1
        else:
            buf = data[i:]
            frame = m.Frame(data_id, 1, buf)
        frame_list.append(frame)
    return frame_list