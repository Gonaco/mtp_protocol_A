import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import message_functions as m
import packetManagement as pm
GPIO.setmode(GPIO.BCM)

RF_CH = [0x10, 0x40]
BR = NRF24.BR_1MBPS
PA = NRF24.PA_LOW


def setup():

    # print("\n-setup-\n")

    pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]  # addresses for TX/RX channels

    GPIO.setup([0, 1, 17, 27], GPIO.OUT, initial=GPIO.LOW)

    ears = NRF24(GPIO, spidev.SpiDev())  # EARS
    mouth = NRF24(GPIO, spidev.SpiDev())  # MOUTH
    ears.begin(1, 27)  # Set spi-cs pin1, and rf24-CE pin 17
    mouth.begin(0, 17)  # Set spi-cs pin0, and rf24-CE pin 27

    ears.setRetries(15, 15)
    ears.setPayloadSize(32)
    ears.setChannel(RF_CH[0])
    mouth.setRetries(15, 15)
    mouth.setPayloadSize(32)
    mouth.setChannel(RF_CH[1])
    
   # ears.setCRCLength(8)
    #mouth.setCRCLength(8)

    ears.setDataRate(BR)
    ears.setPALevel(PA)
    mouth.setDataRate(BR)
    mouth.setPALevel(PA)

    ears.setAutoAck(False)
    ears.enableDynamicPayloads()  # ears.setPayloadSize(32) for setting a fixed payload
    ears.enableAckPayload()
    mouth.setAutoAck(False)
    mouth.enableDynamicPayloads()
    mouth.enableAckPayload()

    mouth.openWritingPipe(pipes[0])
    ears.openReadingPipe(1, pipes[1])

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


def receive(radio, radio2, pipe, frame_received):
    print("\n-receive-\n")
    first_frame = True
    last_frame = False
    review = False
    run = True
    timer = 0
    timer2 = 0
    timer3 = 0
    count = 0
    num_frames_lost = 0
    last_w_id = -1
    storedFrames = {"-2N": "DEFAULT"}
    team = "A"
    window_id = 1
    window_size = 10  # may change
    original_frames_id = []

    while run:
        count = count + 1
        if not first_frame:
            while not radio.available(pipe):
                time.sleep(1 / 1000.0)
                if review:
                    timer = timer + 1
                    if timer == 300:  # TIMEOUT (may change)
                        count = num_frames_lost
                        timer = 0

            recv_buffer = []
            radio.read(recv_buffer, radio.getDynamicPayloadSize())
            rcv = m.Packet()
            rcv.mssg2Pckt(recv_buffer)
            storedFrames, last_w_id = pm.rebuildData(rcv.getID(), rcv.getPayload(), last_w_id, storedFrames, team)

            # In each iteration set to -1 the value of this array located in the received frame ID position
            if rcv.getID() >= len(original_frames_id):
                for i in range(len(original_frames_id), rcv.getID()+1):
                    original_frames_id.append(i)
            original_frames_id[rcv.getID()] = -1

            if count % window_size == 0 and count != 0 and rcv.getEnd() != 1 and not last_frame:
                frames2resend_id = []
                frames2resend_id = find_lost_frames(original_frames_id[last_w_id: count])
                if len(frames2resend_id) == 0:
                    m.sendACK(window_id, 0, radio2)
                else:
                    m.sendNACK(window_id, frames2resend_id, radio2)

                window_id = window_id + 1

                #for i in range((window_size*(window_id+98)), window_size*(window_id+99), 1):
                 #   original_frames_id.append(i)
            
            elif last_frame and count == num_frames_lost and count != 0:
                frames2resend_id = find_lost_frames(original_frames_id[last_w_id:])
                if len(frames2resend_id) == 0:  # All frames are received
                    print("The entire message is received")
                    for j in range(0, 10, 1):
                        m.sendACK(window_id, 1, radio2)
                        while timer2 < 40:
                            time.sleep(1 / 1000.0)
                            timer2 = timer2 + 1
                        timer2 = 0
                    run = False
                else:
                    print('last received and ask to resend')
                    count = 0
                    num_frames_lost = len(frames2resend_id)
                    m.sendNACK(window_id, frames2resend_id, radio2)

            elif rcv.getEnd() == 1 and not last_frame:
                final_id = rcv.getID()
                original_frames_id = original_frames_id[0: final_id+1]  # Set the length of original_frames_id
                last_frame = True
                review = True

                frames2resend_id = find_lost_frames(original_frames_id[last_w_id:])
                if len(frames2resend_id) == 0:  # All frames are received
                    print("The entire message is received the first time")
                    for j in range(0, 10, 1):
                        m.sendACK(window_id, 1, radio2)
                        while timer3 < 40:
                            time.sleep(1 / 1000.0)
                            timer3 = timer3 + 1
                        timer3 = 0
                    run = False
                else:
                    print('we just received last')
                    count = 0
                    num_frames_lost = len(frames2resend_id)
                    m.sendNACK(window_id, frames2resend_id, radio2)

        else:
            #for i in range(0, 100*window_size, 1):
                #original_frames_id.append(i)  # Generate the first 30 original frames ID windows
            for i in range(0, frame_received.getID()+1):
                original_frames_id.append(i)
            
            storedFrames, last_w_id = pm.rebuildData(frame_received.getID(), frame_received.getPayload(), last_w_id, storedFrames, team)
            original_frames_id[frame_received.getID()] = -1
            first_frame = False


def find_lost_frames(vector_id):
    lost_frames_id = []
    for i in range(0, len(vector_id), 1):
        if vector_id[i] != -1:
            lost_frames_id.append(vector_id[i])

    return lost_frames_id


def handshake(radio, radio2, pipe):
    print("\n-handshake-\n")
    done = False
    wait = False
    timer = 0
    frame_received = []
    while not done:
        while not radio.available(pipe):
            time.sleep(1/1000.0)
            if wait:
                timer = timer + 1
                if timer == 300:  # TIMEOUT (may change)
                    m.sendACK(0, 0, radio2)
                    timer = 0

        recv_buffer = []
        radio.read(recv_buffer, radio.getDynamicPayloadSize())
        rcv = m.Packet()
        rcv.mssg2Pckt(recv_buffer)
        if rcv.getTyp() == 0 and rcv.getID() == 0:
            m.sendACK(0, 0, radio2)
            wait = True
        elif rcv.getTyp() == 1 and rcv.getID() == 0:
            GPIO.cleanup()
            done = True
        elif rcv.getTyp() == 3:
            frame_received = rcv
            done = True

    return frame_received
