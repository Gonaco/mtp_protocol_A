import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import message_functions as m

def setup():
    pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]] #addresses for TX/RX channels

    radio = NRF24(GPIO, spidev.SpiDev())
    radio2 = NRF24(GPIO, spidev.SpiDev())
    radio.begin(1, 27) # Set spi-cs pin1, and rf24-CE pin 27
    radio2.begin(0, 17) # Set spi-cs pin0, and rf24-CE pin 17

    radio.setRetries(15,15)
    radio.setPayloadSize(32)
    radio.setChannel(0x60)
    radio2.setRetries(15,15)
    radio2.setPayloadSize(32)
    radio2.setChannel(0x60)

    radio.setDataRate(NRF24.BR_2MBPS)
    radio.setPALevel(NRF24.PA_MAX)
    radio2.setDataRate(NRF24.BR_2MBPS)
    radio2.setPALevel(NRF24.PA_MAX)

    radio.setAutoAck(False)
    radio.enableDynamicPayloads() # radio.setPayloadSize(32) for setting a fixed payload
    radio.enableAckPayload()
    radio2.setAutoAck(False)
    radio2.enableDynamicPayloads()
    radio2.enableAckPayload()

    radio2.openWritingPipe(pipes[0])
    radio.openReadingPipe(1, pipes[1])

    radio2.startListening()
    radio2.stopListening()

    radio2.printDetails()

    radio.startListening()
    return radio, radio2

"""def decide_type()
    recv=m.packet()
    type= recv.getType()
    if type == 0:
        f.receive_sync()
    elif type == 3:
        f.receive_frame()
    elif type == 1:
        f.receive_ack()
    return type
"""

def synchronized(radio, radio2, pipe):
    done = False
    while not done:
        # radio.startListening()
        while not radio.available(pipe):
            time.sleep(1/1000.0)
        print("sync message received")
        recv_buffer = []
        radio.read(recv_buffer, radio.getDynamicPayloadSize())
        rcv = m.Packet()
        rcv.strMssg2Pckt(recv_buffer)
        if rcv.getTyp() == 0:
            if rcv.getID == 0:
                m.sendACK(0,radio2)
                done = True

def receive(radio, radio2):
    first_frame = True
    run = True
    ack = False
    nack = False
    count = 0
    timer = 0
    window_id = 0
    window_size = 10  # may change
    frames2resend_id = []
    frames_id = []
    str = []
    pipe = [0]

    while run:
        count = count + 1
        tmpStr = ""

        while not radio.available(pipe) and timer < 50000:
            time.sleep(1 / 1000.0)
            timer = timer + 1
        if timer == 50000: # Timeout
            if first_frame:
                m.sendACK(0, radio2) # Send the first ACK
            else:
                if ack:
                    m.sendACK(window_id, radio2) # Resend previous ACK
                elif nack:
                    m.sendNACK(window_id, frames2resend_id, radio2) # Resend previous NACK
        timer = 0

        recv_buffer = []
        radio.read(recv_buffer, radio.getDynamicPayloadSize())
        for i in range(0, len(recv_buffer), 1):
            tmpStr = tmpStr + chr(recv_buffer[i])
        rcv = m.Packet()
        rcv.strMssg2Pckt(recv_buffer)
        frames_id.append(rcv.getID)
        str.append(tmpStr)

        if count % window_size == 0:
            window_id = window_id + 1
            # frames2resend_id = [] # Initialize the array to zero or it is not necessary?
            frames2resend_id = find_lost_frames(frames_id[window_size*(window_id-1) : len(count)-1])
            if len(frames2resend_id) == 0:
                m.sendACK(window_id, radio2)
                ack = True
                nack = False
            else:
                m.sendNACK(window_id, frames2resend_id, radio2)
                ack = False
                nack = True

        # CHECK IT because once I receive the frame with flag==1 I'm constantly sending Nacks until all packets
        # are correclty received
        if rcv.getFlag == 1 or rcv.getTyp == 1: # Generate a function getFlag in message_functions
            frames2resend_id = find_lost_frames(frames_id[window_size*(window_id - 1) : len(count)-1])
            if len(frames2resend_id) == 0: # All frames are received
                run = False
            else:
                m.sendNACK(window_id + 1, frames2resend_id, radio2)
                ack = False
                nack = True


    #outfile = open("rx_file.txt", "w")
    aux = ""
    for i in range(0, len(str), 1):
        aux = aux + str[i]
    outfile.write(aux)
    #outfile.close()
    print("The entire message is received")

def end_connection(radio, radio2):

def find_lost_frames(array):
    # Design a function that allows me to know the lost frames
    return lost_frames_id