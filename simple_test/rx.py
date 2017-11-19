
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

from lib_nrf24 import NRF24
import time
import spidev
import re
import math

print("\n-setup-\n")

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]] #addresses for TX/RX channels

ears = NRF24(GPIO, spidev.SpiDev())  # EARS
mouth = NRF24(GPIO, spidev.SpiDev())  # MOUTH
ears.begin(1, 27) # Set spi-cs pin1, and rf24-CE pin 17
mouth.begin(0, 17) # Set spi-cs pin0, and rf24-CE pin 27

ears.setRetries(15,15)
ears.setPayloadSize(32)
ears.setChannel(0x65)
mouth.setRetries(15,15)
mouth.setPayloadSize(32)
mouth.setChannel(0x00)

ears.setDataRate(NRF24.BR_2MBPS)
ears.setPALevel(NRF24.PA_MAX)
mouth.setDataRate(NRF24.BR_2MBPS)
mouth.setPALevel(NRF24.PA_MAX)

ears.setAutoAck(False)
ears.enableDynamicPayloads() # ears.setPayloadSize(32) for setting a fixed payload
ears.enableAckPayload()
mouth.setAutoAck(False)
mouth.enableDynamicPayloads()
mouth.enableAckPayload()

mouth.openWritingPipe(pipes[0])
ears.openReadingPipe(1, pipes[1])

mouth.startListening()
mouth.stopListening()

mouth.printDetails()

ears.startListening()


send = "Oh. Hola!"


while not ears.available([1]):
    print("Listening")

rcv_buffer = []
ears.read(rcv_buffer, ears.getDynamicPayloadSize())
print(rcv_buffer)

mssg_string = ""
for i in range(0,len(rcv_buffer),1):
    mssg_string = mssg_string + chr(rcv_buffer[i])
    
print(mssg_string)

# mouth.write(send)
# print(send)

for i in range(0,50):
    mouth.write(send)
    print(send)

GPIO.cleanup()
