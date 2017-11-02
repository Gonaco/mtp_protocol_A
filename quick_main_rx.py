import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import message_functions as m

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]] #addresses for TX/RX channels

radio = NRF24(GPIO, spidev.SpiDev())
radio2 = NRF24(GPIO, spidev.SpiDev())
radio.begin(1, 27) # Set spi-cs pin1, and rf24-CE pin 27
radio2.begin(0, 17) # Set spi-cs pin0, and rf24-CE pin 17

radio.setRetries(15, 15)
radio.setPayloadSize(32)
radio.setChannel(0x60)
radio2.setRetries(15, 15)
radio2.setPayloadSize(32)
radio2.setChannel(0x60)

radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_MAX)
radio2.setDataRate(NRF24.BR_2MBPS)
radio2.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
radio.enableDynamicPayloads()  # radio.setPayloadSize(32) for setting a fixed payload
radio.enableAckPayload()
radio2.setAutoAck(True)
radio2.enableDynamicPayloads()
radio2.enableAckPayload()

radio2.openWritingPipe(pipes[0])
radio2.openReadingPipe(1, pipes[1])

radio2.startListening()
radio2.stopListening()
radio2.printDetails()

radio2.startListening()

c = 1
num = 0
outfile = open("rx_file.txt", "w")
run = True
str = ""
while run:
    akpl_buf = [c, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8]
    pipe = [0]
    while not radio2.available(pipe) and num < 500:
        time.sleep(10000 / 1000000.0)
        num = num + 1
        if num == 499:
            run = False
    num = 0
    if run == True:
        recv_buffer = []
        radio2.read(recv_buffer, radio2.getDynamicPayloadSize())
        print ("Received:")

        for i in range(0, len(recv_buffer), 1):
            str = str + chr(recv_buffer[i])
        print (str)

        c = c + 1
        if (c & 1) == 0:
            radio2.writeAckPayload(1, akpl_buf, len(akpl_buf))
            print ("Loaded payload reply:"),
            print (akpl_buf)
        else:
            print ("(No return payload)")
    else:
        outfile.write(str)
        outfile.close()
        print("The message is received")