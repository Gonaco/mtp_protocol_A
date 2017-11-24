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

from threading import Thread

# NETWORK CONSTANTS
PAYLOAD_LENGTH = 31
HEADER_LENGTH = 1
TDATA_MAX = TACK_MAX = 0.2                         # Data and ACK frames timeout (in seconds)
# TDATA = TACK = 0.0005                                     # Waiting time in order to transmit
TDATA = TACK = 0.005
TCTRL = TINIT = 0                           # Control frame and initialization random timeouts (in seconds)
TMAX = 120                                  # Max time for network mode (in seconds)
START_TIME = 0


PLOAD_SIZE = 32                             # Payload size corresponding to data in one frame (32 B max)
HDR_SIZE = 1                                # Header size inside payload frame

# TRANSCEIVER CONSTANTS
RF_CH = 0x64                        # UL & DL channels
PWR_LVL = NRF24.PA_MIN                     # Transceiver output (HIGH = -6 dBm + 20 dB)
BRATE = NRF24.BR_250KBPS                    # 250 kbps bit rate

SEND_ACK1 = 0
SEND_ACK2 = 0
SEND_ACK3 = 0

ACKED = {m.B_TEAM : 0, m.C_TEAM : 0, m.D_TEAM : 0}


PIPES = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]  # addresses for TX/RX channels
EARS_PIPE = [1]

ACTIVE_TEAM = m.A_TEAM

PKTS_RCVD = 0

last_w_id_B = -1
last_w_id_C = -1
last_w_id_D = -1

F_CMPLTD = 0
# POS_MAX = 

storedFrames = {"-2N": "DEFAULT"}  # NO ENTIENDO ESTO

def setup():

    print("\n-setup-\n")

    GPIO.setup([0,1,17,27], GPIO.OUT, initial=GPIO.LOW)

    ears = NRF24(GPIO, spidev.SpiDev())  # EARS
    mouth = NRF24(GPIO, spidev.SpiDev())  # MOUTH
    ears.begin(1, 27)  # Set spi-cs pin1, and rf24-CE pin 17
    mouth.begin(0, 17)  # Set spi-cs pin0, and rf24-CE pin 27

    # ears.setRetries(15, 15)
    ears.setPayloadSize(32)     # SURE?
    ears.setChannel(RF_CH)
    # mouth.setRetries(15, 15)
    mouth.setPayloadSize(32)    # SURE?
    mouth.setChannel(RF_CH)

    ears.setDataRate(BRATE)
    ears.setPALevel(PWR_LVL)
    mouth.setDataRate(BRATE)
    mouth.setPALevel(PWR_LVL)

    ears.setAutoAck(False)
    ears.enableDynamicPayloads()  # ears.setPayloadSize(32) for setting a fixed payload
    # ears.enableAckPayload()
    mouth.setAutoAck(False)
    mouth.enableDynamicPayloads()
    # mouth.enableAckPayload()

    mouth.openWritingPipe(PIPES[0])
    ears.openReadingPipe(EARS_PIPE[0], PIPES[1])

    if not mouth.isPVariant():
        # If radio configures correctly, we confirmed a "plus" (ie "variant") nrf24l01+
        # Else print diagnostic stuff & exit.
        mouth.printDetails()
        # (or we could always just print details anyway, even on good setup, for debugging)
        print ("NRF24L01+ not found.")
        return

    if not ears.isPVariant():
        # If radio configures correctly, we confirmed a "plus" (ie "variant") nrf24l01+
        # Else print diagnostic stuff & exit.
        ears.printDetails()
        # (or we could always just print details anyway, even on good setup, for debugging)
        print ("NRF24L01+ not found.")
        return
    
    mouth.startListening()
    mouth.stopListening()

    mouth.printDetails()

    ears.startListening()

    return ears, mouth



def subSend(r,s):
    r.write(s)


    
def listen(ears, timer):
    print("\n-Listening-\n")

    tmr_bgn = time.time()
    while (not ears.available(EARS_PIPE) and time.time() < (tmr_bgn + timer)):
        #Do nothing
        pass

    if ears.available(EARS_PIPE):
        return True
    else:
        return False

def receivingData():
    
    # We are gonna write down what we have received
    print("\n-Receiving Data-\n")
    
    recv_buffer = []
    ears.read(recv_buffer, ears.getDynamicPayloadSize())  # CHECK IT
    rcv = m.DataFrame()
    if rcv.mssg2Pckt(recv_buffer):

        print(rcv)

        if(rcv.getRx() == m.A_TEAM): #If the Data Frame is for us, we write it down

            if(ACTIVE_TEAM == m.B_TEAM):
                storedFrames, last_w_id_B = pm.rebuildData(rcv.getPos(), rcv.getPayload(), last_w_id_B, storedFrames, ACTIVE_TEAM)
                SEND_ACK1 = 1

            elif(ACTIVE_TEAM == m.C_TEAM):
                storedFrames, last_w_id_C = pm.rebuildData(rcv.getPos(), rcv.getPayload(), last_w_id_C, storedFrames, ACTIVE_TEAM)
                SEND_ACK2 = 1

            elif(ACTIVE_TEAM == m.D_TEAM):
                storedFrames, last_w_id_D = pm.rebuildData(rcv.getPos(), rcv.getPayload(), last_w_id_D, storedFrames, ACTIVE_TEAM)
                SEND_ACK3 = 1

        else:
            print("PACKET FOR OTHER TEAM")
            return

    else:

        print("ERROR. THIS PACKET IS NOT RECOGNIZED")
        return


# def active(t,ears,mouth):
def active(ears,mouth):
    # In this function, our furby has won the medium so it will send the first control frame.
    # Then, it will wait for the three teams to send as back their corresponding control fram acknowleding us.
    # If it has received 2 or more ACKs it wil start sending Data Frames

    print("\n-Active Mode-\n")

    ACTIVE_TEAM = m.A_TEAM
    
    # completed_files = 0
    data_id = 0
    print("Sending our Control Frame\n")
    # control = m.ControlFrame(m.B_TEAM, SEND_ACK1, SEND_ACK2, SEND_ACK3)  # FILL WITH ACK FOR THE RX PKTS
    control = m.ControlFrame()
    mouth.write(control.__str__())
    # send_thrd = Thread (target = subSend, args = (mouth,control.__str__()))
    # send_thrd.start()

    # Reset the ACKS
    SEND_ACK1 = 0
    SEND_ACK2 = 0
    SEND_ACK3 = 0
    
    # Let's see if anyone answers back...
    answers = 0
    tmr_bgn = time.time()
    
    # If we've received AT LEAST TWICE the frame that we've sent, we sent ALL the data frames
    while (answers != 3 and time.time() < (START_TIME + TACK)):
        
        if ears.available(EARS_PIPE):
            print("Receiving ACK?")
            recv_buffer = []
            ears.read(recv_buffer, ears.getDynamicPayloadSize())  # CHECK IT
            rcv = m.ControlFrame()
            rcv.strMssg2Pckt(recv_buffer)
            if (rcv.getTx() == m.A_TEAM):
                answers += 1
                
    if (answers < 1):
        print("NO ANSWER")
        return
    
    else:
        print("Sending")
    #     for team in t:
    #         team_data = t[team]

    #         if ACKED[team] < len(team_data):

    #             frame = m.DataFrame(team, ACKED[team], team_data[ACKED[team]])    
    #             mouth.write(frame.__str__())
    #             print("Sent:")
    #             print(frame)
    #         else:
    #             print("File Completed")
    #             F_CMPLTD += 1
                
    #         time.sleep(TDATA)


def passive(ears,mouth):
    # In this function, another team's furby has won the medium
    # We will resend the control frame that we've receive changing the ACK bit that corresponds to our team
    # Stay listening for our data frame

    print("\n-Passive Mode-\n")

    # PKTS_RCVD = 0

    # Taking the packet
    recv_buffer = []
    ears.read(recv_buffer, ears.getDynamicPayloadSize()) #CHECK IT
    print(recv_buffer)
    rcv = m.ControlFrame()
    print(rcv)
    if rcv.mssg2Pckt(recv_buffer):  # Check if is a Control Frame or a Data Frame

        print(rcv)
        
        ACTIVE_TEAM = rcv.getTx()
        NEXT_TEAM = rcv.getNxt()

        print("we received other team's Control Frame")
        # TDATA = 25 / 1000.0

        # Depending on Who has send us the Control Frame, our ACK could be in any place    
        if rcv.getTx() == m.B_TEAM:
            print("Team B is active")
            if(rcv.ack1 == 1): #B is acknowleding our data frame
                ACKED[m.B_TEAM] += 1
            rcv.ack1 = 0
            rcv.ack2 = 0
            rcv.ack3 = 0

        elif rcv.getTx() == m.C_TEAM:
            print("Team C is active")
            if (rcv.ack1 == 1):  # C is acknowleding our data frame
                ACKED[m.C_TEAM] += 1
            rcv.ack1 = 0
            rcv.ack2 = 0
            rcv.ack3 = 0

        elif rcv.getTx() == m.D_TEAM:
            print("Team D is active")
            if(rcv.ack1 == 1): #D is acknowleding our data frame
                ACKED[m.D_TEAM] += 1
            rcv.ack1 = 0
            rcv.ack2 = 0
            rcv.ack3 = 0

        time.sleep(random.uniform(0, TACK))
        mouth.write(rcv.__str__()) #Send the ACK
        # send_thrd = Thread (target = subSend, args = (mouth,rcv.__str__()))
        # send_thrd.start()
        

        print("ACK sent")
        tmr_bgn = time.time()
        while time.time() < (START_TIME + TDATA_MAX):
            print("Waiting for Data")
            if ears.available(EARS_PIPE):
                receivingData()
                
            
    # else:

    #     print("Data Received")

    #     rcv = m.DataFrame()
        
    #     if rcv.mssg2Pckt(recv_buffer):
    #         receivingData()
    #     else:
    #         print("ERROR. THIS PACKET IS NOT RECOGNIZED")
        
        
                
                
    # return acked_B, acked_C, acked_D, last_w_id_B, last_w_id_C, last_w_id_D



def network_mode(ears, mouth, files):

    print("\n-Network Mode-\n")

    START_TIME = time.time()

    random.seed(int(START_TIME))

    print(START_TIME)
    
    beginning = True

    texts = {m.B_TEAM : files[0], m.C_TEAM: files[1], m.D_TEAM: files[2]}

    for team in texts:
        split_str = pm.splitData(texts[team], PAYLOAD_LENGTH)
        texts[team] = split_str

    while (time.time() < START_TIME + TMAX) and (F_CMPLTD != 6):
        
        if beginning:
            TINIT = random.uniform(5, 10)
            timer = TINIT
            beginning = False

        elif ACTIVE_TEAM == m.D_TEAM:

            timer = 0
            
        else:
            TCTRL = random.uniform(1, 2)
            timer = TCTRL
    
        
        if (listen(ears, timer)):
            # Something received -> Passive Mode
            
            passive(ears, mouth)
            
        else:
            # Something received -> Active Mode
            
            active(texts,ears,mouth)
            # ACTIVE_TEAM = m.B_TEAM

        
