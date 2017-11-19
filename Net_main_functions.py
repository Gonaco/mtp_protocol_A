#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import random
import time
import math
import datetime
import message_functions as m
import packetManagement as pm
import splitData as s



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


    return 0


##################DEBUG CODE BELOW############################
def network_mode(f):
    run = True
    while run:
    radio.startListening()
    paysize = 31
    frame_list_B = build_list(f[0], paysize)
    id_last_B = frame_list_B[-1].getID()
    frame_list_C = build_list(f[1], paysize)
    id_last_C = frame_list_C[-1].getID()
    frame_list_D = build_list(f[2], paysize)
    id_last_D = frame_list_D[-1].getID()
    pipe=[1]
    TMAX = 120
    TX_CMPLT = 0
    RX_CMPLT = 0
    TCTRLMAX = 1
    TINIT = random.uniform(5, 10)
    TCTRL = random.uniform(1, 2)
    listen(radio,TINIT)
    start_time = time.time()
    while (TX_CMPLT < 3 and RX_CMPLT < 3 and time.time() < (start_time + TMAX)):
        if (not radio.available):
            TX_CMPLT = active(f)
            # WAIT_CONTROL
            listen(radio,TCTRLMAX) #We have to implement a Tmax to wait until the next team send us its Control Frame
            if(radio.available):
                ack_B,ack_C,ack_D, writen_B, writen_C, writen_D = passive()
                if(TX_CMPLT == 3 and ack_B == id_last_B  and ack_C == id_last_C and ack_D == id_last_D and writen_B ==  and writen_C ==  and writen_D == ):
                    print("\n-THE END-\n")
                    return 0 #If we have send all the files, received confirmation for all of them and writen down everything...We are done!
            else:
                listen(radio,TCTRL)
                if (radio.available):
                    passive()
                #The else case is that the timer run out and we can send our control frame again, so start the while again
        else:
            passive()

def listen(radio, timer):
    print("\n-Listening-\n")

    while (not radio.available(pipe) and time.time() < (start_time + timer)):
        #Do nothing
        pass

def active(f):
    # In this function, our furby has won the medium so it will send the first control frame.
    # Then, it will wait for the three teams to send as back their corresponding control fram acknowleding us.
    # If it has received 2 or more ACKs it wil start sending Data Frames

    print("\n-Active Mode-\n")
    paysize = 31
    files = {'B': f[0], 'C': f[1], 'D': f[2]}
    completed_files = 0
    TACK = 25 / 1000.0
    data_id = 0
    print("Sending our Control Frame\n")
    control = m.ControlFrame()
    radio.write(control.__str__())
    # Let's see if anyone answers back...
    answers = 0
    start_time = time.time()
    # If we've received AT LEAST TWICE the frame that we've sent, we sent ALL the data frames
    while (answers != 3 and time.time() < (start_time + TACK)):  # I THINK THAT BEFORE THIS WHILE OR INSIDE IT, WE SHOULD CHECK THE RADIO.AVAILABLE IN ORDET TO NOT READ NOTHING
        recv_buffer = []
        radio.read(recv_buffer, radio.getDynamicPayloadSize())  # CHECK IT
        rcv = m.ControlFrame()
        rcv.strMssg2Pckt(recv_buffer)
        if (rcv.getTx() == m.A_TEAM):
            answers += 1
    if (answers < 2):
        return 0
    else:
        for team in files:
            data = files.get(team).read()
            if synchronized():  # WHY SYNCHRONIZED FUNCTION??
                print("Sending the file for team", team)
                for i in range(0, len(data), paysize):
                    if (i + paysize) < len(data):
                        buf = data[i:i + paysize]
                        print("sending full packets")
                    else:
                        buf = data[i:]
                        print("FILE COMPLETED")
                        completed_files += 1
                    frame = m.DataFrame(team, data_id, buf)
                    radio.write(frame.__str__())
                    print("Sent:")
                    print(frame)
        data_id += 1
        return completed_files


def passive():
    # In this function, another team's furby has won the medium
    # We will resend the control frame that we've receive changing the ACK bit that corresponds to our team
    # Stay listening for our data frame

    print("\n-Passive Mode-\n")

    last_w_id_B = -1
    last_w_id_C = -1
    last_w_id_D = -1
    storedFrames = {"-2N": "DEFAULT"}
    team = "A"
    active = "B" #We are supposing that the first time to send us a Data Fram is teamB, if not, it will be changed
    acked_B = 0
    acked_C = 0
    acked_D = 0
    recv_buffer = []
    radio.read(recv_buffer, radio.getDynamicPayloadSize()) #CHECK IT
    rcv = m.ControlFrame()
    rcv.strMssg2Pckt(recv_buffer)
    print("we received other team's Control Frame")
    TDATA = 25 / 1000.0
    # Depending on Who has send us the Control Frame, our ACK could be in any place
    if rcv.getTx() == m.B_TEAM:
        print("Team B is active mode")
        active = "B"
        if(rcv.ack3 == 1): #B is acknowleding our data frame
            acked_B += 1
            rcv.ack1 = 0
            rcv.ack2 = 0
            rcv.ack3 = 1

    elif rcv.getTx() == m.C_TEAM:
        print("Team C is active mode")
        active = "C"
        if (rcv.ack2 == 1):  # C is acknowleding our data frame
            acked_C += 1
            rcv.ack1 = 0
            rcv.ack2 = 1
            rcv.ack3 = 0

    elif rcv.getTx() == m.D_TEAM:
        print("Team D is active mode")
        active = "D"
        if(rcv.ack1 == 1): #D is acknowleding our data frame
            acked_D += 1
            rcv.ack1 = 1
            rcv.ack2 = 0
            rcv.ack3 = 0

    radio.write(rcv.__str__()) #Send the ACK

    listen(radio,TDATA) #Waiting 25ms for our data packet
    if (radio.available):
        #We are gonna write down what we have received
        recv_buffer = []
        radio.read(recv_buffer, radio.getDynamicPayloadSize())  # CHECK IT
        rcv = m.DataFrame
        rcv.strMssg2Pckt(recv_buffer)
        if(rcv.getRx() == team): #If the Data Fram is for us, we write it down
            if(active == "B"):
                storedFrames, last_w_id_B = pm.rebuildData(rcv.getPos(), rcv.getPayload(), last_w_id_B, storedFrames, active)
            elif(active == "C"):
                storedFrames, last_w_id_C = pm.rebuildData(rcv.getPos(), rcv.getPayload(), last_w_id_C, storedFrames, active)
            elif(active == "D"):
                storedFrames, last_w_id_D = pm.rebuildData(rcv.getPos(), rcv.getPayload(), last_w_id_D, storedFrames, active)
    return acked_B, acked_C, acked_D, last_w_id_B, last_w_id_C, last_w_id_D


def build_list(file, paysize):
    print("\n-build_list-\n")  ##Debbuging issues.
    data_id = 0
    frame_list = []
    data = file.read()
    file_length = len(data)
    payload = ''
    num = math.ceil(file_length / paysize)
    for i in range(0, int(num - 1)):
        payload = s.splitData(data_id, file)
        frame = m.Frame(data_id, 0, payload)
        data_id = + 1
        frame_list.append(frame)
    # the last packet should have end flag to 1
    payload = s.splitData(data_id, file)
    frame = m.Frame(data_id, 1, payload)
    frame_list.append(frame)
    return frame_list

def synchronized(radio, radio2, pipe):
    print("\n-synchronized-\n")  # Debbuging issues.
    done = False
    sync = m.SYNC(0)
    num = 0
    # print(sync.extractHeader())
    while not done:
        radio.write(sync.__str__())
        radio2.startListening()
        # while not radio2.available(pipe) and num < 400: # WHY A TIMER (400) HERE?
        # time.sleep(1 / 1000.0)
        # num = num + 1
        # if num != 400:
        # print("we received something before time out")
        # rcv_buffer = []
        # radio2.read(rcv_buffer, radio2.getDynamicPayloadSize())
        # rcv = m.Packet()
        # rcv.mssg2Pckt(rcv_buffer)
        # if rcv.getTyp() == 1:
        #     if rcv.getID() == 0:
        #         done = True

        while not radio2.available(pipe):
            # do nothing
            pass

        print("we received something before time out")
        rcv_buffer = []
        radio2.read(rcv_buffer, radio2.getDynamicPayloadSize())
        rcv = m.Packet()
        rcv.mssg2Pckt(rcv_buffer)
        if rcv.getTyp() == 1:
            if rcv.getID() == 0:
                done = True
