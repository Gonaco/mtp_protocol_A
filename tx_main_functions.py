#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import message_functions as m
import re


def setup():
    pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]  # addresses for TX/RX channels

    radio2 = NRF24(GPIO, spidev.SpiDev())
    radio = NRF24(GPIO, spidev.SpiDev())
    radio.begin(1, 17)  # Set spi-cs pin1, and rf24-CE pin 27
    radio2.begin(0, 27)  # Set spi-cs pin0, and rf24-CE pin 17

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

    timeout = time.time() + 0.1
    return radio, radio2


##################DEBUG CODE BELOW############################
def transmit(radio, radio2, file):
    run = True
    paysize = 27  # may change
    repeat = False
    window_id = 1
    window_size = 10  # may change
    last_sent = -1
    data = file.read()
    frame_list = build_list(data, paysize)
    radio2.startListening()
    nack_list = []
    nack_len = 0
    partial_window = 0
    finished = False
    while run:
        if not repeat:
            if (last_sent + window_size) < len(frame_list):
                for i in range(0, window_size):
                    frame = frame_list[last_sent + 1]
                    radio.write(frame.__str__())
                    last_sent = +1
            else:
                for i in range(last_sent + 1, len(frame_list)):
                    frame = frame_list[last_sent + 1]
                    radio.write(frame.__str__())
                    last_sent = +1
                    finished = True
        else:
            # To Do: manage NACKs
            nack_len = len(nack_list)
            if nack_len < window_size:
                # we send a mix of Nack and next ids
                for i in range(0, len(nack_list)):
                    #we send nack
                    next_id = nack_list[i]
                    frame = frame_list[next_id]
                    radio.write(frame.__str__())
                    nack_list.pop[i]
                for i in range(0, partial_window):
                    #we send next frames
                    frame = frame_list[last_sent + 1]
                    radio.write(frame.__str__())
                    last_sent = +1
            else:
                #To Do: case where we have more Nacks than window size
                for i in range(0, window_size):
                    #we send the first 10 nacks and eliminate them from the list
                    next_id = nack_list[i]
                    frame = frame_list[next_id]
                    radio.write(frame.__str__())
                    nack_list.pop[i]

        if radio2.available():
            rcv_buffer = []
            radio2.read(rcv_buffer, radio2.getDynamicPayloadSize())
            rcv = m.Packet()
            rcv.strMssg2Pckt(rcv_buffer)
            if rcv.getTyp() == 2:
                # nack received
                repeat = True
                # read payload and store IDs in list
                nack_string = rcv.getPayload()
                temp_nack_list = re.split(',', nack_string)
                temp_nack_list.pop(len(nack_list) - 1)
                nack_list = nack_list + temp_nack_list
            elif finished:
                if rcv.getTyp() == 1:
                    # I store the ID of the last ACK rx set me
                    id_last = rcv.getID()
                    run = False;
    return id_last


def synchronized(radio, radio2, pipe):
    done = False
    sync = m.SYNC(0)
    num=0
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
            if rcv.getTyp() == 1:
                if rcv.getID == 0:
                    done = True
    return done


def end_connection(radio, radio2, pipe, id):
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
            rcv.strMssg2Pckt(rcv_buffer)
            if rcv.getTyp() == 1:
                # we have the id of the last packet an rx will send un an ack with the next id
                if rcv.getID == id + 1:
                    radio2.stopListening()
                    done = True


def build_list(data, paysize):
    data_id = 1
    frame_list = []
    for i in range(0, len(data), paysize):
        if (i + paysize) < len(data):
            buf = data[i:i + paysize]
            frame = m.Frame(data_id, 0, buf)
            i = +1
        else:
            buf = data[i:]
            frame = m.Frame(data_id, 1, buf)
        frame_list.append(frame)
    return frame_list
