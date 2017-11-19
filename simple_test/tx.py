import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import re
import math

from threading import Thread

# def listening():
#     global rcvd
#     while True:
#         rcvd = False
#         rcvd = ears.available([0])
#         time.sleep(1)

def subSend(r,s):
    r.write(s)
    


print("\n-setup-\n")  ##Debbuging issues.
pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]  # addresses for TX/RX channels

ears = NRF24(GPIO, spidev.SpiDev())
mouth = NRF24(GPIO, spidev.SpiDev())
mouth.begin(1, 27)  # Set spi-cs pin1, and rf24-CE pin 27
ears.begin(0, 17)  # Set spi-cs pin0, and rf24-CE pin 17

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

send = "Psst"

send_thrd = Thread (target = subSend, args = (mouth,send))

while not ears.available([0]):
    if not thrd.isAlive():
        print(send)
        send_thrd.start()

rcv_buffer = []
ears.read(rcv_buffer, ears.getDynamicPayloadSize())
print(rcv_buffer)

mssg_string = ""
for i in range(0,len(rcv_buffer),1):
    mssg_string = mssg_string + chr(rcv_buffer[i])
    
print(mssg_string)

# while not ears.available(0):
#     pass

# print()
