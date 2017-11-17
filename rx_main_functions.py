import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import message_functions as m
import rebuildData

def setup():
    pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]] #addresses for TX/RX channels

    radio = NRF24(GPIO, spidev.SpiDev())
    radio2 = NRF24(GPIO, spidev.SpiDev())
    radio.begin(1, 17) # Set spi-cs pin1, and rf24-CE pin 17
    radio2.begin(0, 27) # Set spi-cs pin0, and rf24-CE pin 27

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
        while not radio.available(pipe):
            time.sleep(1/1000.0)
        print("sync message received")
        recv_buffer = []
        radio.read(recv_buffer, radio.getDynamicPayloadSize())
        rcv = m.Packet()
        rcv.mssg2Pckt(recv_buffer)
        if rcv.getTyp() == 0:
            if rcv.getID() == 0:
                m.sendACK(0,radio2)
                done = True

def receive(radio, radio2, pipe):
    first_frame = True
    last_frame = False
    run = True
    ack = False
    nack = False
    count = 0
    timer = 0
    num_frames_lost = 0
    last_w_id = -1
    storedFrames = {"-2N" : "DEFAULT"}
    team = "A"
    window_id = 1
    window_size = 10  # may change
    original_frames_id = []
    frames2resend_id = []
    pipe = [0]

    while run:
        count = count + 1

        while not radio.available(pipe) and timer < 50000:
            time.sleep(1 / 1000.0)
            timer = timer + 1
        if timer == 50000: # Timeout
            if first_frame:
                m.sendACK(0, radio2) # Send the first ACK again

            else:
                if ack:
                    m.sendACK(window_id, radio2) # Resend previous ACK
                elif nack:
                    m.sendNACK(window_id, frames2resend_id, radio2) # Resend previous NACK
        timer = 0

        if first_frame:
            for i in range(0, (2*window_size)-1, 1):
                original_frames_id.append(i) # Generate the first 2 original frames ID windows
            first_frame = False

        recv_buffer = []
        rcv = m.Packet()
        rcv.mssg2Pckt(recv_buffer)
        storedFrames, last_w_id = rebuildData(rcv.getID, rcv.getPayload, last_w_id, storedFrames, team)

        original_frames_id.insert(rcv.getID,0) # In each iteration set to zero the value of this array located in the received frame ID position (The first frame has ID=0 and is located in the position 0 of the array)

        if count % window_size == 0:
            frames2resend_id = []
            frames2resend_id = find_lost_frames(original_frames_id[window_size*(window_id-1) : len(count)-1])
            if len(frames2resend_id) == 0:
                m.sendACK(window_id, radio2)
                ack = True
                nack = False
            else:
                m.sendNACK(window_id, frames2resend_id, radio2)
                ack = False
                nack = True

            window_id = window_id + 1

            for i in range ((window_size*window_id), window_size*(window_id+1)-1, 1):
                original_frames_id.append(i) # Generate the original frames ID for the the i+1 window

        if rcv.getEnd() == 1 and last_frame == False:
            final_id = rcv.getID()
            original_frames_id = original_frames_id[0:final_id-1] # Set the length of original_frames_id
            last_frame = True

            frames2resend_id = find_lost_frames(original_frames_id[window_size*(window_id - 1): len(original_frames_id)])
            if len(frames2resend_id) == 0:  # All frames are received
                run = False
                print("The entire message is received")
            else:
                count = 0
                num_frames_lost = len(frames2resend_id)
                m.sendNACK(window_id, frames2resend_id, radio2)
                ack = False
                nack = True

        if last_frame == True and count == num_frames_lost:
            frames2resend_id = find_lost_frames(original_frames_id[window_size*(window_id - 1): len(original_frames_id)])
            if len(frames2resend_id) == 0:  # All frames are received
                run = False
                print("The entire message is received")
            else:
                count = 0
                num_frames_lost = len(frames2resend_id)
                m.sendNACK(window_id, frames2resend_id, radio2)
                ack = False
                nack = True

    return final_id

def end_connection(radio, radio2, pipe):


def find_lost_frames(array):
    lost_frames_id=[]
    for i in range (0, len(array), 1):
        if array(i) != -1:
            lost_frames_id.append(i)

    return lost_frames_id