#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import random
import time
import datetime
import message_functions as m


def setup():
    pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]  # addresses for TX/RX channels

    radio2 = NRF24(GPIO, spidev.SpiDev())
    radio = NRF24(GPIO, spidev.SpiDev())
    radio.begin(1, 27)  # Set spi-cs pin1, and rf24-CE pin 27
    radio2.begin(0, 17)  # Set spi-cs pin0, and rf24-CE pin 17

    time.sleep(1)
    radio.setRetries(15, 15)
    radio.setPayloadSize(32)
    radio.setChannel(0x60)
    radio2.setRetries(15, 15)
    radio2.setPayloadSize(32)
    radio2.setChannel(0x60)

    radio2.setDataRate(NRF24.BR_2MBPS)
    radio2.setPALevel(NRF24.PA_MAX)
    radio.setDataRate(NRF24.BR_2MBPS)
    radio.setPALevel(NRF24.PA_MAX)

    radio.setAutoAck(False)
    radio.enableDynamicPayloads()  # radio.setPayloadSize(32) for setting a fixed payload
    radio.enableAckPayload()
    radio2.setAutoAck(False)
    radio2.enableDynamicPayloads()
    radio2.enableAckPayload()

    radio.openWritingPipe(pipes[1])
    radio.openReadingPipe(1, pipes[0])
    radio.printDetails()

    paysize = 30  # size of payload we send at once
    timeout = time.time() + 0.1
    return 0


##################DEBUG CODE BELOW############################
def transmit(f):
    run = True
    while run:
        radio.startListening()
        pipe=[1]
        #We wait a random time between 5 and 10 seconds
        Tinit=random.randint(5,10)
        time.sleep(Tinit)
        #If we haven't received any Control Frame yet, we send our Control Frame
        recv_buffer = []
        radio.read(recv_buffer, radio.getDynamicPayloadSize())
        rcv = m.ControlFrame()
        rcv.strMssg2Pckt(recv_buffer)
        if not radio.available(pipe):
            print("Sending our Control Frame\n")
            control=m.ControlFrame()
            radio.write(control.__str__())
            #Let's see if anyone answers back...If we've received at least once the frame that we've sent...
            recv_buffer = []
            radio.read(recv_buffer, radio.getDynamicPayloadSize()) #CHECK IT
            rcv = m.ControlFrame()
            rcv.strMssg2Pckt(recv_buffer)
            if(rcv.getTx() == control.tx):
                #We send the data frames in order to the teams that have answered back
                answers=0
                start_time = datetime.datetime.now()
                while(answers != 3):
                    time_delta = datetime.now() - start_time
                    if(time_delta.seconds <= 0,025)
                        if (rcv.getAck1() == 1):
                            files = {'B': f[0]}
                            answers += 1
                        if(rcv.getAck2() == 1):
                            files['C'] = f[1]
                            answers += 1
                        if (rcv.getAck3() == 1):
                            files['D'] = f[2]
                            answers += 1
                    else
                        radio.write(control.__str__())
                data = 1;
                data_id = 1
                while (data != ''):
                    for team in files:
                        data = file.get(team).read()
                        if synchronized():
                            print("Sending the file for team", team)
                            for i in range(0, len(data), paysize):
                                if (i + paysize) < len(data):
                                    buf = data[i:i + paysize]
                                    print("sending full packets")
                                else:
                                    buf = data[i:]
                                    run = False
                                frame = m.Frame(data_id, 0, buf)
                                radio.write(frame)
                                print("Sending our Control Frame\n")
                                frame.send(radio)
                                print("Sent:"),
                                print(frame)
                    data_id += 1
            end_connection()
            return 0 # 0 means that the conversation has gone OK
        elif():
            #This else means that I have received a Control Frame from other team
            # I resend that control frame to the transmitter and I wait Tdata=25ms so they can send us the Data Frames
            print("we received other team's Control Frame")
            control = m.ControlFrame()
            if (rcv.getTx()=1): #Depending on Who has send us the Control Frame, our ACK could be in any place
                control.ack1 =0
                control.ack2 =0
                control.ack3 =1
            elif(rcv.getTx()=2):
                control.ack1 =0
                control.ack2 =1
                control.ack3 =0
            else:
                control.ack1=1
                control.ack2=0
                control.ack3=0
            radio.write(control.__str__())
            time.sleep(25/1000.0)
        else:
            #I keep waiting for Control Frames during a Tctrl and then I resend my own
            Tinit = random.randint(1, 2)
            time.sleep(Tinit)
            return 1 # 1 means that the process has to be restarted (TupperA will call this script again)


def synchronized():
    done = False
    sync = m.SYNC(0, '')
    # print(sync.extractHeader())
    sync.send(radio)
    radio.startListening()
    if radio.available():
        radio.read(buffer, radio.getPayloadSize())
        print("Sync done")
        done = True
    return done;


def end_connection():
    ack = m.ACK(0, 0)  # for ending connection we send ACK with ID 0 #CHECK IT
    ack.send(radio)
    radio.startListening()
    if radio.available():
        radio.read(buffer, radio.getPayloadSize())
    print("Done sending the file! Exiting!")

    return;
