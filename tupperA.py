import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import sys

def TX(f_name):

    t_file = open(f_name, "r"))
    correct = main_tx(t_file)
    t_file.close()
    return correct


def RX():

    r_file = open("rx_file.txt","w"))
    correct = main_rx(r_file)
    r_file.close
    
def NT(argv):

    tx_file_buffer = []
    rx_file_buffer = []
    for f in range(1,len(argv)):
        tx_file_buffer.append(open(argv[f], "r"))
        rx_file_buffer.append(open("rx_file"+str(f)+".txt","w"))

    correct = main_nt(tx_file_buffer, rx_file_buffer)

    for f in range(1,len(argv)):
        tx_file_buffer.append(open(argv[f], "r"))
        rx_file_buffer.append(open("rx_file"+str(f)+".txt","w"))

    return correct
    
    
def main(argv):
    
    cont = 1
    options = {'tx':TX(argv[1]),
               'rx':RX(),
               'network':NT(argv)}

    while (cont != 0):    
        
        if (...):
            cont = options['tx']
        ...
    
if __name__ == "__main__":
    main(sys.argv)

