#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import message_functions as m
import packetManagement as p
import re
import math
GPIO.setmode(GPIO.BCM)

RF_CH = [0x00, 0x32]
BR = NRF24.BR_250KBPS
PA = NRF24.PA_MIN

def setup():
    # print("\n-setup-\n")  # Debbuging issues.
    pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]  # addresses for TX/RX channels


    GPIO.setup([0, 1, 17, 27], GPIO.OUT, initial=GPIO.LOW)

    ears = NRF24(GPIO, spidev.SpiDev())
    mouth = NRF24(GPIO, spidev.SpiDev())
    mouth.begin(1, 27)  # Set spi-cs pin1, and rf24-CE pin 27 ¿?SURE¿? NOT AS IN THE QUICK MODE
    ears.begin(0, 17)  # Set spi-cs pin0, and rf24-CE pin 17 ¿?SURE¿? NOT AS IN THE QUICK MODE

    time.sleep(1)

    mouth.setRetries(15, 15)
    mouth.setPayloadSize(32)
    mouth.setChannel(RF_CH[0])
    ears.setRetries(15, 15)
    ears.setPayloadSize(32)
    ears.setChannel(RF_CH[1])

    ears.setDataRate(BR)
    ears.setPALevel(PA)
    mouth.setDataRate(BR)
    mouth.setPALevel(PA)

    mouth.setAutoAck(False)
    mouth.enableDynamicPayloads()  # mouth.setPayloadSize(32) for setting a fixed payload
    mouth.enableAckPayload()
    ears.setAutoAck(False)
    ears.enableDynamicPayloads()
    ears.enableAckPayload()

    mouth.openWritingPipe(pipes[1])
    ears.openReadingPipe(1, pipes[0])

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

    mouth.printDetails()
    mouth.startListening()
    mouth.stopListening()
    ears.startListening()
    timeout = time.time() + 0.1
    #print('finish set up')
    return mouth, ears


# #################DEBUG CODE BELOW############################
def transmit(radio, radio2, archivo, pipe):
    print("\n-transmit-\n")  # Debbuging issues.
    run = True
    paysize = m.FRAME_PAYLOAD_BYTES_LENGTH  # may change
    repeat = False
    last_window = -1
    window_size = 10  # may change
    last_sent = -1
    # data = file.read()
    frame_list = build_list(archivo, paysize)
    radio2.startListening()
    nack_list = []
    nack_len = 0
    partial_window = 0
    finished = False
    id_last = frame_list[-1].getID()
    #print('before starting the run loop')
    while run:
        #print('after while run')
        if not finished:
            #print('if not finished')
            if not repeat:
                last_sent, finished = send_window(frame_list, last_sent, window_size, radio, finished)
            else:
                #print('we have nacks')
                nack_len = len(nack_list)
                if nack_len < window_size:
                    #print('we have mix window')
                    # we send a mix of Nack and next ids
                    for i in range(0, nack_len):
                        # we send nack
                        # print(nack_list[0])
                        next_id = nack_list[0]
                        frame = frame_list[int(next_id)]
                        # print('%s we send frame' % next_id)
                        radio.write(frame.__str__())
                        nack_list.pop(0)
                    # we send the rest of the window
                    repeat = False
                    partial_window=window_size-nack_len
                    last_sent, finished = send_window(frame_list, last_sent, partial_window, radio, finished)
                    partial_window=0
                else:
                    #print('we only send nacks')
                    for i in range(0, window_size):
                        # we send the first 10 nacks and eliminate them from the list
                        next_id = nack_list[0]
                        frame = frame_list[int(next_id)]
                        #print('%s we send frame' % next_id)
                        radio.write(frame.__str__())
                        nack_list.pop(0)
            last_window = last_window+1
            # after we send, we look for nacks
            if radio2.available(pipe):
                # print('we have things to read')
                rcv_buffer = []
                radio2.read(rcv_buffer, radio2.getDynamicPayloadSize())
                rcv = m.Packet()
                rcv.mssg2Pckt(rcv_buffer)
                # wether I finished or not I want to look for nacks
                if rcv.getTyp() == 2:
                    repeat=True
                    nack_list = process_nacks(rcv, nack_list)
                rcv=''
        else:
            #print('if finished')
            num = 0
            while not radio2.available(pipe) and num < 400:
                time.sleep(1 / 1000.0)
                num = num + 1
            if num < 400:
                # print('after if')
                #print(rcv.getTyp())
                #we recived something
                if radio2.available(pipe):
                    print('we have things to read')
                    time.sleep(0.5)
                    rcv_buffer = []
                    radio2.read(rcv_buffer, radio2.getDynamicPayloadSize())
                    rcv = m.Packet()
                    rcv.mssg2Pckt(rcv_buffer)
                    #print(rcv)
                    #print('I received a packet of type %s' % rcv.getTyp())
                    #print('The ID of the packet is %s' % rcv.getID())
                    # wether I finished or not I want to look for nacks
                    if rcv.getTyp() == 2:
                        nack_list = process_nacks(rcv, nack_list)
                        nack_len = len(nack_list)
                        if nack_len < window_size:
                            #print('we do not send full window')
                            for i in range(0, nack_len):
                                # we send nack
                                # print(nack_list[0])
                                next_id = nack_list[0]
                                frame = frame_list[int(next_id)]
                                #print('%s we send frame' % next_id)
                                radio.write(frame.__str__())
                        else:
                            #print('we send full window')
                            for i in range(0, window_size):
                                # we send the first 10 nacks and eliminate them from the list
                                next_id = nack_list[0]
                                frame = frame_list[int(next_id)]
                                #print('%s we send frame' % next_id)
                                radio.write(frame.__str__())
                                nack_list.pop(0)
                    print('I sent last so I will check for ack')
                    #time.sleep(2)
                    # if I don't have nacks, I only care if I finished
                    # if rx send ack we stop running, if we didn't finish, just write next window
                    if rcv.getTyp() == 1 and rcv.getEnd() == 1:
                        print('there is ack')
                        run = False
                    if rcv.getTyp() == 0:
                        time.sleep(10)
                    rcv = ''
            else:
                #timeot
                frame = frame_list[-1]
                # print('%d we send last frame again')
                radio.write(frame.__str__())

    return id_last


def synchronized(radio, radio2, pipe):
    # print("\n-synchronized-\n")  # Debbuging issues.
    done = False
    while not done:
        # print('sending sync')
        num = 0
        m.sendSYNC(0, radio)
        radio2.startListening()
        while not radio2.available(pipe) and num < 400:  # WHY A TIMER (400) HERE?
            time.sleep(1 / 1000.0)
            num = num + 1
        if num < 400:
            # print("we received something before time out")
            rcv_buffer = []
            radio2.read(rcv_buffer, radio2.getDynamicPayloadSize())
            rcv = m.Packet()
            rcv.mssg2Pckt(rcv_buffer)
            if rcv.getTyp() == 1 and rcv.getID() == 0:
                radio2.stopListening()
                done = True
        # else:
        #     # print('did not receive ack') 


def end_connection(radio, radio2, pipe, last_id):
    print("\n-end_connection-\n")  # Debbuging issues.
    #done = False
    #while not done:
        # print('sending ack')
        #num = 0
    for i in range(0, 10):
        m.sendACK(0, 0, radio)
    GPIO.cleanup()
        #radio2.startListening()
        #while not radio2.available(pipe) and num < 400:
         #   time.sleep(1 / 1000.0)
          #  num = num + 1
        #if num < 400:
            # print("we received something before time out")
         #   rcv_buffer = []
          #  radio2.read(rcv_buffer, radio2.getDynamicPayloadSize())
           # rcv = m.Packet()
            #rcv.mssg2Pckt(rcv_buffer)
      #      if rcv.getTyp() == 1 and rcv.getID() == last_id:
       #         radio2.stopListening()
        #        done = True
        # else:
        #     print('did not receive ack')


def build_list(archivo, paysize):
    # print("\n-build_list-\n")  # Debbuging issues.
    data_id = 0
    frame_list = []
    payload_list = []
    payload_list = p.splitData(archivo, paysize)
    #print('Just after split data, I print first payload')
    #payload_list[0]
    # print('%s is the payload returned by carol' % payload)
    for i in range(0, int(len(payload_list)-1)):
        payload = payload_list[i]
        frame = m.Frame(data_id, 0, payload)
        frame_list.append(frame)
        data_id = data_id + 1
    payload = payload_list[-1]
    frame = m.Frame(data_id, 1, payload)
    frame_list.append(frame)
    #print('I created the list, this is the payload of the first frame')
    #print(frame_list[0].getPayload())
    #time.sleep(2)
    return frame_list


def send_window(frame_list, last_sent, window_size, radio, finished):
    # print("\n-send_window-\n")  # Debbuging issues.
    if (last_sent + window_size) < len(frame_list):
        #print('we send a window')
        for i in range(0, window_size):
            frame = frame_list[last_sent + 1]
            #print('%d we send frame' % last_sent)
            radio.write(frame.__str__())
            last_sent = last_sent+1
    else:
        print('we send last window')
        for i in range(last_sent + 1, len(frame_list)):
            frame = frame_list[last_sent + 1]
            radio.write(frame.__str__())
            last_sent = last_sent+1
            finished = True
            #This is to leave time for the rx to answer
            time.sleep(0.4)
    #time.sleep(2)
    return last_sent, finished

def process_nacks(rcv, nack_list):
    #print('nacks arrived')
    # nack received
    # read payload and store IDs in list
    nack_string = rcv.getPayload()
    # print('this is the string of nacks we receive %s' % nack_string)
    #time.sleep(2)
    temp_nack_list = re.split(',', nack_string)
    temp_nack_list.pop(-1)
    nack_list = nack_list + temp_nack_list
    return nack_list
