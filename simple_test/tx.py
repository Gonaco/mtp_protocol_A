import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import message_functions as m
import splitData as s
import re
import math

print("\n-setup-\n")  ##Debbuging issues.
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

send = "Psst"


while not radio2.available(0):
    radio.write(send)

rcv_buffer = []
radio2.read(rcv_buffer, radio2.getDynamicPayloadSize())

for i in range(0,len(rcv_buffer),1):
    mssg_string = mssg_string + chr(rcv_buffer[i])
    
print(mssg_string)

# while not radio2.available(0):
#     pass

# print()
