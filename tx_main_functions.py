#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import message_functions as m
import splitData as s
import re
import math


def setup():
    print("\n-setup-\n")  ##Debbuging issues.
    pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]  # addresses for TX/RX channels

    # radio2 = NRF24(GPIO, spidev.SpiDev())
    # radio = NRF24(GPIO, spidev.SpiDev())
    # radio.begin(1, 17)  # Set spi-cs pin1, and rf24-CE pin 27 ¿?SURE¿? NOT AS IN THE QUICK MODE
    # radio2.begin(0, 27)  # Set spi-cs pin0, and rf24-CE pin 17 ¿?SURE¿? NOT AS IN THE QUICK MODE

    # time.sleep(1)               # WHY sleep here?
    # radio.setRetries(15, 15)
    # radio.setPayloadSize(32)
    # radio.setChannel(0x60)
    # radio2.setRetries(15, 15)
    # radio2.setPayloadSize(32)
    # radio2.setChannel(0x60)

    # radio2.setDataRate(NRF24.BR_2MBPS)
    # radio2.setPALevel(NRF24.PA_MAX)
    # radio.setDataRate(NRF24.BR_2MBPS)
    # radio.setPALevel(NRF24.PA_MAX)

    # radio.setAutoAck(False)
    # radio.enableDynamicPayloads()  # radio.setPayloadSize(32) for setting a fixed payload
    # radio.enableAckPayload()
    # radio2.setAutoAck(False)
    # radio2.enableDynamicPayloads()
    # radio2.enableAckPayload()

    # radio.openWritingPipe(pipes[1])
    # radio2.openReadingPipe(1, pipes[0])
    # radio.printDetails()

    # radio2.startListening()

    # timeout = time.time() + 0.1
    # return radio, radio2

    ears = NRF24(GPIO, spidev.SpiDev())
    mouth = NRF24(GPIO, spidev.SpiDev())
    mouth.begin(1, 27)  # Set spi-cs pin1, and rf24-CE pin 27 ¿?SURE¿? NOT AS IN THE QUICK MODE
    ears.begin(0, 17)  # Set spi-cs pin0, and rf24-CE pin 17 ¿?SURE¿? NOT AS IN THE QUICK MODE

    time.sleep(1)

    mouth.setRetries(15, 15)
    mouth.setPayloadSize(32)
    mouth.setChannel(0x60)
    ears.setRetries(15, 15)
    ears.setPayloadSize(32)
    ears.setChannel(0x65)

    ears.setDataRate(NRF24.BR_2MBPS)
    ears.setPALevel(NRF24.PA_MAX)
    mouth.setDataRate(NRF24.BR_2MBPS)
    mouth.setPALevel(NRF24.PA_MAX)

    mouth.setAutoAck(False)
    mouth.enableDynamicPayloads()  # mouth.setPayloadSize(32) for setting a fixed payload
    mouth.enableAckPayload()
    ears.setAutoAck(False)
    ears.enableDynamicPayloads()
    ears.enableAckPayload()

    mouth.openWritingPipe(pipes[1])
    ears.openReadingPipe(1, pipes[0])
    mouth.printDetails()

    mouth.startListening()
    mouth.stopListening()

    ears.startListening()
    
    timeout = time.time() + 0.1
    return mouth, ears


##################DEBUG CODE BELOW############################
def transmit(radio, radio2, file):
    print("\n-transmit-\n")  ##Debbuging issues.
    run = True
    paysize = 27  # may change
    repeat = False
    window_id = 1
    window_size = 10  # may change
    last_sent = -1
    # data = file.read()
    frame_list = build_list(file, paysize)
    radio2.startListening()
    nack_list = []
    nack_len = 0
    partial_window = 0
    finished = False
    id_last = frame_list[-1].getID()
    print('before starting the run loop')
    while run:
        if not repeat:
            last_sent, finished = send_window(frame_list, last_sent, window_size, radio, finished)
        else:
            print('we have nacks')
            nack_len = len(nack_list)
            if nack_len < window_size:
                print('we have mix window')
                # we send a mix of Nack and next ids
                for i in range(0, len(nack_list)):
                    # we send nack
                    next_id = nack_list[i]
                    frame = frame_list[next_id]
                    radio.write(frame.__str__())
                    nack_list.pop(i)
                # we send the rest of the window
                last_sent, finished = send_window(frame_list, last_sent, partial_window, radio, finished)
            else:
                print('we only send nacks')
                for i in range(0, window_size):
                    # we send the first 10 nacks and eliminate them from the list
                    next_id = nack_list[i]
                    frame = frame_list[next_id]
                    radio.write(frame.__str__())
                    nack_list.pop(i)
        # after we send, we look for nacks
        if radio2.available():
            print('we have things to read')
            rcv_buffer = []
            radio2.read(rcv_buffer, radio2.getDynamicPayloadSize())
            rcv = m.Packet()
            rcv.mssg2Pckt(rcv_buffer)
            # wether I finished or not I want to look for nacks
            if rcv.getTyp() == 2:
                print('nacks arrived')
                # nack received
                repeat = True
                # read payload and store IDs in list
                nack_string = rcv.getPayload()
                temp_nack_list = re.split(',', nack_string)
                temp_nack_list.pop(len(nack_list) - 1)
                nack_list = nack_list + temp_nack_list
            elif finished:
                print('I sent last so I will check for ack')
                # if I don't have nacks, I only care if I finished
                # if rx send ack we stop running, if we didn't finish, just write next window
                if rcv.getTyp() == 1:
                    print('there is ack')
                    # I store the ID of the last ACK rx set me
                    # id_last = rcv.getID()
                    run = False
    return id_last


def synchronized(radio, radio2, pipe):
    print("\n-synchronized-\n")  #Debbuging issues.
    done = False
    sync = m.SYNC(0)
    num = 0
    # print(sync.extractHeader())
    while not done:
        radio.write(sync.__str__())
        radio2.startListening()
        while not radio2.available(pipe) and num < 400: # WHY A TIMER (400) HERE?
            time.sleep(1 / 1000.0)
            num = num + 1
        if num != 400:
            print("we received something before time out")
            rcv_buffer = []
            radio2.read(rcv_buffer, radio2.getDynamicPayloadSize())
            rcv = m.Packet()
            rcv.mssg2Pckt(rcv_buffer)
            if rcv.getTyp() == 1:
                if rcv.getID() == 0:
                    done = True



def end_connection(radio, radio2, pipe, last_id):
    print("\n-end_connection-\n")  ##Debbuging issues.
    done = False
    ack = m.ACK(0)  # for ending connection we send ACK with ID 0
    radio.write(ack.__str__())
    radio2.startListening()
    while not done:
        while not radio2.available(pipe) and num < 400:
            time.sleep(1 / 1000.0)
            num = num + 1
        if num != 400:
            print("we received something before time out")
            rcv_buffer = []
            radio2.read(rcv_buffer, radio2.getDynamicPayloadSize())
            rcv = m.Packet()
            rcv.mssg2Pckt(rcv_buffer)
            if rcv.getTyp() == 1:
                # we have the id of the last packet an rx will send un an ack with the next id
                if rcv.getID() == last_id + 1:
                    radio2.stopListening()
                    done = True


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


def send_window(frame_list, last_sent, window_size, radio, finished):
    print("\n-send_window-\n")  ##Debbuging issues.
    if (last_sent + window_size) < len(frame_list):
        print('we send a window')
        for i in range(0, window_size):
            frame = frame_list[last_sent + 1]
            radio.write(frame.__str__())
            last_sent = +1
    else:
        print('we send last window')
        for i in range(last_sent + 1, len(frame_list)):
            frame = frame_list[last_sent + 1]
            radio.write(frame.__str__())
            last_sent = +1
            finished = True
    return last_sent, finished
