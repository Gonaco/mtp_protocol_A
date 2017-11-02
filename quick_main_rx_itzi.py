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
radio.enableDynamicPayloads() # radio.setPayloadSize(32) for setting a$
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

c=1
num=0
outfile=open("rx_file.txt","w")
run=True
str = ""
while run:
    akpl_buf = [c,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8]
    pipe = [0]
    while not radio.available(pipe) and num<500:
        time.sleep(10000/1000000.0)
        num=num+1
        if num ==499:
            run=False
    num=0
    if run==True:
        recv_buffer = []
        radio.read(recv_buffer, radio.getDynamicPayloadSize())
        print ("Received:")
        #recv_packet= m.Packet()
        for i in range(6,len(recv_buffer),1):
            str = str + chr(recv_buffer[i])
        print (str)
        #recv_packet.strMssg2Pckt(recv_buffer)
	    #print(recv_packet)
	    #print(recv_packet.getPayload())

        #ack=m.ACK(c, "")
        #ack.send(radio2)
        radio2.write(akpl_buf)
        print ("ACK SENT"),
    else:
        outfile.write(str)
        outfile.close()
        print("The message is received")
