import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import message_functions as m
import packetManagement as pm
GPIO.setmode(GPIO.BCM)


def setup():

    print("\n-setup-\n")

    pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]  # addresses for TX/RX channels

    # radio = NRF24(GPIO, spidev.SpiDev())
    # radio2 = NRF24(GPIO, spidev.SpiDev())
    # radio.begin(1, 17) # Set spi-cs pin1, and rf24-CE pin 17
    # radio2.begin(0, 27) # Set spi-cs pin0, and rf24-CE pin 27

    # radio.setRetries(15,15)
    # radio.setPayloadSize(32)
    # radio.setChannel(0x60)
    # radio2.setRetries(15,15)
    # radio2.setPayloadSize(32)
    # radio2.setChannel(0x60)

    # radio.setDataRate(NRF24.BR_2MBPS)
    # radio.setPALevel(NRF24.PA_MAX)
    # radio2.setDataRate(NRF24.BR_2MBPS)
    # radio2.setPALevel(NRF24.PA_MAX)

    # radio.setAutoAck(False)
    # radio.enableDynamicPayloads() # radio.setPayloadSize(32) for setting a fixed payload
    # radio.enableAckPayload()
    # radio2.setAutoAck(False)
    # radio2.enableDynamicPayloads()
    # radio2.enableAckPayload()

    # radio2.openWritingPipe(pipes[0])
    # radio.openReadingPipe(1, pipes[1])

    # radio2.startListening()
    # radio2.stopListening()

    # radio2.printDetails()

    # radio.startListening()
    # return radio, radio2

    GPIO.setup([0,1,17,27], GPIO.OUT, initial=GPIO.LOW)

    ears = NRF24(GPIO, spidev.SpiDev())  # EARS
    mouth = NRF24(GPIO, spidev.SpiDev())  # MOUTH
    ears.begin(1, 27)  # Set spi-cs pin1, and rf24-CE pin 17
    mouth.begin(0, 17)  # Set spi-cs pin0, and rf24-CE pin 27

    ears.setRetries(15, 15)
    ears.setPayloadSize(32)
    ears.setChannel(0x60)
    mouth.setRetries(15, 15)
    mouth.setPayloadSize(32)
    mouth.setChannel(0x65)

    ears.setDataRate(NRF24.BR_2MBPS)
    ears.setPALevel(NRF24.PA_MAX)
    mouth.setDataRate(NRF24.BR_2MBPS)
    mouth.setPALevel(NRF24.PA_MAX)

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
    run = True
    count = 0
    final_id = 0
    num_frames_lost = 0
    last_w_id = -1
    storedFrames = {"-2N": "DEFAULT"}
    team = "A"
    window_id = 1
    window_size = 10  # may change
    original_frames_id = []

    while run:
        count = count + 1

        """if first_frame:
            for i in range(0, (2*window_size)-1, 1):
                original_frames_id.append(i)  # Generate the first 2 original frames ID windows
            storedFrames, last_w_id = pm.rebuildData(frame_received.getID(), frame_received.getPayload(), last_w_id, storedFrames, team)
            original_frames_id.insert(frame_received.getID(), -1)
            first_frame = False"""

        if not first_frame:
            while not radio.available(pipe):
                time.sleep(1 / 1000.0)

            print("I have got a frame")
            recv_buffer = []
            radio.read(recv_buffer, radio.getDynamicPayloadSize())
            rcv = m.Packet()
            rcv.mssg2Pckt(recv_buffer)

            print ("the frame is %s" % rcv.getID())
            storedFrames, last_w_id = pm.rebuildData(rcv.getID(), rcv.getPayload(), last_w_id, storedFrames, team)

            # In each iteration set to -1 the value of this array located in the received frame ID position
            original_frames_id.insert(rcv.getID(), -1)

            if count % window_size == 0:
                frames2resend_id = []
                frames2resend_id = find_lost_frames(original_frames_id[window_size*(window_id-1): count-1])
                if len(frames2resend_id) == 0:
                    m.sendACK(window_id, radio2)
                else:
                    m.sendNACK(window_id, frames2resend_id, radio2)

                window_id = window_id + 1

                for i in range((window_size*window_id), window_size*(window_id+1)-1, 1):
                    original_frames_id.append(i)  # Generate the original frames ID for the the i+1 window

            if rcv.getEnd() == 1 and not last_frame:
                final_id = rcv.getID()
                original_frames_id = original_frames_id[0:final_id-1]  # Set the length of original_frames_id
                last_frame = True

                frames2resend_id = find_lost_frames(original_frames_id[window_size*(window_id-1): len(original_frames_id)])
                if len(frames2resend_id) == 0:  # All frames are received
                    run = False
                    print("The entire message is received")
                else:
                    count = 0
                    num_frames_lost = len(frames2resend_id)
                    m.sendNACK(window_id, frames2resend_id, radio2)

            if last_frame and count == num_frames_lost:
                frames2resend_id = find_lost_frames(original_frames_id[window_size*(window_id-1): len(original_frames_id)])
                if len(frames2resend_id) == 0:  # All frames are received
                    run = False
                    print("The entire message is received")
                else:
                    count = 0
                    num_frames_lost = len(frames2resend_id)
                    m.sendNACK(window_id, frames2resend_id, radio2)

        else:
            for i in range(0, (2 * window_size) - 1, 1):
                original_frames_id.append(i)  # Generate the first 2 original frames ID windows
            print ("the frame is %s" % frame_received.getID())
            storedFrames, last_w_id = pm.rebuildData(frame_received.getID(), frame_received.getPayload(),
                                                     last_w_id, storedFrames, team)
            original_frames_id.insert(frame_received.getID(), -1)
            first_frame = False

    return final_id


def find_lost_frames(vector_id):
    print("\n-find_lost_frames-\n")
    lost_frames_id = []
    for i in range(0, len(vector_id)-1, 1):
        if vector_id[i] != -1:
            lost_frames_id.append(vector_id[i])

    return lost_frames_id


def handshake(radio, radio2, pipe, packet_id):
    print("\n-handshake-\n")
    done = False
    wait = False
    timer = 0
    frame_received = []
    while not done:
        while not radio.available(pipe):
            # print("\n-listening-\n")
            time.sleep(1/1000.0)
            if wait:
                timer = timer + 1
                if timer == 400:  # TIMEOUT
                    m.sendACK(packet_id, radio2)
                    print("Resend ACK")
                    timer = 0

        recv_buffer = []
        radio.read(recv_buffer, radio.getDynamicPayloadSize())
        rcv = m.Packet()
        rcv.mssg2Pckt(recv_buffer)
        print(rcv)
        if rcv.getTyp() == 0 and rcv.getID() == 0:
            print("sync message received")
            m.sendACK(packet_id, radio2)
            wait = True
        elif rcv.getTyp() == 1 and rcv.getID() == 0:
            print("ACK message received")
            m.sendACK(packet_id, radio2)
            done = True
        elif rcv.getTyp() == 3 and rcv.getID() == 0:
            print("I have got the first frame")
            frame_received = rcv
            done = True

    return frame_received
