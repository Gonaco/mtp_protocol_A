
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import message_functions as m
import splitData as s
import re
import math


print("\n-setup-\n")

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


send = "Oh. Hola!"

while not radio.available(1):
    pass

rcv_buffer = []
radio.read(rcv_buffer, radio.getDynamicPayloadSize())
for i in range(0,len(rcv_buffer),1):
    mssg_string = mssg_string + chr(rcv_buffer[i])
    
print(mssg_string)
radio2.write(send)
