import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import sys
from os import listdir

TX_RX_SWITCH = 29
NW_SWITCH = 31
ON_OFF_SWITCH = 33
ON_OFF_LED = 36
NW_LED = 38
TX_LED = 40

IRQS = [35,37]                  # WE ARE NOT USING THEM, BUT JUST IN CASE

FREE_PINS = [3,5,7,8,10,12,14,15,16,17,18,20,22,25,27,28,30,32,34,39] # IN ORDER TO SET THEM AS OUTPUT AND AVOID ERRORS


def initPorts():

    GPIO.setmode(GPIO.BOARD)

    # INPUTS

    GPIO.setup(TX_RX_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    GPIO.setup(NW_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    GPIO.setup(ON_OFF_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(ON_OFF_SWITCH, GPIO.BOTH)
    GPIO.add_event_callback(ON_OFF_SWITCH, run)

    GPIO.setup(IRQS, GPIO.IN)

    # OUTPUTS

    GPIO.setup(ON_OFF_LED, GPIO.OUT)
    
    GPIO.setup(NW_LED, GPIO.OUT)
    
    GPIO.setup(TX_LED, GPIO.OUT)

    # Just for being sure that there are no errors with the pins as input
    GPIO.setup(FREE_PINS, GPIO.OUT)

def loadFiles(argv):

    print("\n-loadFiles-\n")

    files = []

    if len(argv) > 1:
        
        # In case of using terminal to load te files

        for i in range(1,len(argv)-1):

            filename = argv[i]
            if ".txt" in filename:
                files.append(open(filename, 'r'))
            

    else:

        # In case of using the automatic moe to load the files
            
        for filename in listdir("input_files"):
            if ".txt" in filename:
                files.append(open(filename, 'r'))

    return files


def initInterruptions():

    GPIO.add_event_detect(TX_RX_SWITCH, GPIO.BOTH)
    GPIO.add_event_callback(TX_RX_SWITCH, tx_rx)

    GPIO.add_event_detect(NW_SWITCH, GPIO.RISING)
    GPIO.add_event_callback(NW_SWITCH, NT)


def tx_rx():

    
    
    if GPIO.input(TX_RX_SWITCH):
        TX()
    else:
        RX()

def TX(t_file=files[0]):

    print('\n-TX_mode-\n')

    main_tx(t_file)


def RX():

    print('\n-RX_mode-\n')

    main_rx()
    
    
def NT(tx_file_buffer=files):

    print('\n-NT_mode-\n')

    main_nt(tx_file_buffer)


def run():

    if (GPIO.input(ON_OFF_SWITCH)):
        print("\n-Running-\n")
        initInterruptions()
        
    else:
        print("\n-Closing-\n")
        GPIO.remove_event_detect(TX_RX_SWITCH)
        GPIO.remove_event_detect(NW_SWITCH)
        
    
def main(argv):

    # cont = 1

    files = []

    initPorts()

    files = loadFiles(argv)

    # # options = {'tx':TX(argv[1]),
    # #            'rx':RX(),
    # #            'network':NT(argv)}


    # while (cont != 0):
        
    #     # if (...):
    #     #     cont = options['tx']
    #     # ...


        
    # Closing
    
    GPIO.cleanup()
        
if __name__ == "__main__":
    main(sys.argv)

