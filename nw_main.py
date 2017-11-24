import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import random

import Net_main_functions as nw
import time

# ears, mouth = nw.setup()

# NETWORK CONSTANTS
PAYLOAD_LENGTH = 31
HEADER_LENGTH = 1
TDATA_MAX = TACK_MAX = 0.2                         # Data and ACK frames timeout (in seconds)
TDATA = TACK = 0.0005                                     # Waiting time in order to transmit
TCTRL = TINIT = 0                           # Control frame and initialization random timeouts (in seconds)
TMAX = 120                                  # Max time for network mode (in seconds)
START_TIME = 0


PLOAD_SIZE = 32                             # Payload size corresponding to data in one frame (32 B max)
HDR_SIZE = 1                                # Header size inside payload frame

# TRANSCEIVER CONSTANTS
RF_CH = 0x64                        # UL & DL channels
PWR_LVL = NRF24.PA_MIN                     # Transceiver output (HIGH = -6 dBm + 20 dB)
BRATE = NRF24.BR_250KBPS                    # 250 kbps bit rate


PIPES = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]  # addresses for TX/RX channels
EARS_PIPE = [1]




GPIO.setup([0,1,17,27], GPIO.OUT, initial=GPIO.LOW)
mouth = NRF24(GPIO, spidev.SpiDev())  # MOUTH
mouth.begin(0, 17)  # Set spi-cs pin0, and rf24-CE pin 27
mouth.setRetries(15, 15)
mouth.setPayloadSize(32)    # SURE?
mouth.setChannel(RF_CH)
mouth.setDataRate(BRATE)
mouth.setPALevel(PWR_LVL)
mouth.setAutoAck(False)
mouth.enableDynamicPayloads()
mouth.openWritingPipe(PIPES[0])
if not mouth.isPVariant():
    # If radio configures correctly, we confirmed a "plus" (ie "variant") nrf24l01+
    # Else print diagnostic stuff & exit.
    mouth.printDetails()
    # (or we could always just print details anyway, even on good setup, for debugging)
    print ("NRF24L01+ not found.")
mouth.startListening()
mouth.stopListening()
mouth.printDetails()

timer = 1

# while True:
#     if (nw.listen(ears, timer)):
#         nw.passive(ears,mouth)
#     else:
#         print("Timeout")

# while True:
    
#     # nw.active(ears,mouth)
#     message = "Christian putamo"
#     mouth.write(message)
#     print(message)
#     time.sleep(0.001)
#     if (nw.listen(ears, timer)):
#         print ("ACK received")

#     else:
#         print("Timeout")


while True:

    mouth.write("abcdefghijklmnopqrstuvwxyz")
    

# f = open("tx_file.txt", 'r')

# files = [f,f,f]

# nw.network_mode(ears,mouth,files)
