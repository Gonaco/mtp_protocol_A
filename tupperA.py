import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import sys

def loadReadFiles(argv, tx_files_buffer):
    rx_file_buffer = []
    for f in range(1,len(argv)):
        tx_file_buffer.append(open(argv[f], "r"))
        rx_file_buffer.append(open("rx_file"+str(f)+".txt","w"))
    
def main(argv):
    tx_file_buffer = []
    rx_file_buffer = loadFile(argv, tx_file_buffer)
    

    
    
    

if __name__ == "__main__":
    main(sys.argv)

