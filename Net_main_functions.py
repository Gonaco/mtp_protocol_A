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

    run = True
    while run:
    radio.startListening()
    pipe=[1]
    TMAX = 120
    TX_CMPLT=0
    RX_CMPLT=0
    TINIT = random.uniform(5, 10)
    listen(radio,TINIT)
    while (TX_CMPLT < 3 and RX_CMPLT < 3 and time.time() < (start_time + TMAX)):
        if (not radio.available):
            active()
            # WAIT_CONTROL
            rx_ctrl, packet = received_ctrl()
            if (rx_ctrl):
                # Control received. TX and NEXT updated.
                t_send_ack = random.uniform(0, 0.1)
                time.sleep(t_send_ack)
                # Send ACK
                pasive()
                #The else case is that the timer run out and we can send our control frame again, so start the while again
        else:
            pasive()

def listen(radio, timer):
    print("\n-Listening-\n")

    while (not radio.available(pipe) and time.time() < timer):
        #Do nothing

    # if radio.available(pipe):
    #     recv_buffer = []
    #     rcv = m.C
    #     radio.read(recv_buffer, radio.getDynamicPayloadSize())


def active():
    # In this function, our furby has won the medium so it will send the first control frame.
    # Then, it will wait for the three teams to send as back their corresponding control fram acknowleding us.
    # If it has received 2 or more ACKs it wil start sending Data Frames

    print("\n-Active Mode-\n")

    files = {'B': f[0], 'C': f[1], 'D': f[2]}
    TACK = 25 / 1000.0
    print("Sending our Control Frame\n")
    control = m.ControlFrame()
    radio.write(control.__str__())
    # Let's see if anyone answers back...
    answers = 0
    start_time = time.time()
    # If we've received AT LEAST TWICE the frame that we've sent, we sent ALL the data frames
    while (answers != 3 and time.time() < (start_time + TACK)):
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
                    frame.send(radio)
                    print("Sent:"),
                    print(frame)
        return 0


def passive():
    # In this function, another team's furby has won the medium
    # We will resend the control frame that we've receive changing the ACK bit that corresponds to our team
    # Stay listening for our data frame

    print("\n-Passive Mode-\n")

    recv_buffer = []
    radio.read(recv_buffer, radio.getDynamicPayloadSize()) #CHECK IT
    rcv = m.ControlFrame()
    rcv.strMssg2Pckt(recv_buffer)
    print("we received other team's Control Frame")
    TDATA = 25 / 1000.0

    # Depending on Who has send us the Control Frame, our ACK could be in any place
    if rcv.getTx() == m.B_TEAM:
        print("Team B is active mode")
        rcv.ack1 = 0
        rcv.ack2 = 0
        rcv.ack3 = 1
        
    elif rcv.getTx() == m.C_TEAM:
        print("Team C is active mode")
        rcv.ack1 = 0
        rcv.ack2 = 1
        rcv.ack3 = 0
        
    elif rcv.getTx() == m.D_TEAM:
        print("Team D is active mode")
        rcv.ack1 = 1
        rcv.ack2 = 0
        rcv.ack3 = 0
        
    radio.write(rcv.__str__()) #Send the ACK

    time.sleep(TDATA) #Waiting 25ms for our data packet

# def received_ctrl():
#     TCTRL = random.uniform(1, 2)
#     ctrl_rx = False

#     start_time = time.time()
#     packet = PKT()
#     # While if still not TCTRL but something (wrong) received
#     while (time.time() < start_time + TCTRL and not ctrl_rx):
#         if (radio_Rx.available(0)):
#             # Something received
#             packet.read_pkt()
#             if (packet.is_CTRL()):
#                 # ACK info updated in read_pkt
#                 ctrl_rx = True

#     return ctrl_rx, packet
