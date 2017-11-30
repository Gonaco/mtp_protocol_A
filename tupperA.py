import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import sys
from os import listdir
from main_nw import main as main_nw
from main_tx import main_tx
from main_rx import main_rx

TX_RX_SWITCH = 5  # 29
NW_SWITCH = 12 # 32
ON_OFF_SWITCH = 13 # 33
ON_OFF_LED = 16 # 36
NW_LED = 20 # 38
TX_LED = 21 # 40

IRQS = [19,26] # [35,37]                  # WE ARE NOT USING THEM, BUT JUST IN CASE

FREE_PINS = [2,3,4,6,14,15,18,22,23,24,25] # [3,5,7,8,10,12,15,16,18,22,31] # IN ORDER TO SET THEM AS OUTPUT AND AVOID ERRORS

LAST_PACKET = 1

INIT = True


def initPorts(init):

    GPIO.setmode(GPIO.BCM)

    # INPUTS

    GPIO.setup(TX_RX_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    GPIO.setup(NW_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    GPIO.setup(ON_OFF_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    if init:
        GPIO.add_event_detect(ON_OFF_SWITCH, GPIO.BOTH)
        GPIO.add_event_callback(ON_OFF_SWITCH, on_off)
        init = False

    GPIO.setup(IRQS, GPIO.IN)

    # OUTPUTS

    GPIO.setup(ON_OFF_LED, GPIO.OUT)
    
    GPIO.setup(NW_LED, GPIO.OUT)
    
    GPIO.setup(TX_LED, GPIO.OUT)

    # Just for being sure that there are no errors with the pins as input
    GPIO.setup(FREE_PINS, GPIO.OUT)

    return init


    
# def loadFiles(argv):

    
def loadFiles():
    print("\n-loadFiles-\n")
    files = []

    # if len(argv) > 1:
        
    #     # In case of using terminal to load te files

    #     for i in range(1,len(argv)-1):

    #         filename = argv[i]
    #         if ".txt" in filename:
    #             files.append(open(filename, 'r'))
            

    # else:

    #     # In case of using the automatic moe to load the files
            
    #     for filename in listdir("input_files"):
    #         if ".txt" in filename:
    #             files.append(open(filename, 'r'))

    # return files

    for filename in listdir("/home/pi/mtp_protocol_A/input_files"):
        if ".txt" in filename:
            files.append(open("/home/pi/mtp_protocol_A/input_files/"+filename, 'r'))


# def initInterruptions():

#     GPIO.add_event_detect(TX_RX_SWITCH, GPIO.BOTH)
#     GPIO.add_event_callback(TX_RX_SWITCH, tx_rx)

#     GPIO.add_event_detect(NW_SWITCH, GPIO.RISING)
#     GPIO.add_event_callback(NW_SWITCH, NT)



def TX(t_file):

    print('\n-TX_mode-\n')

    main_tx(t_file)


def RX():

    print('\n-RX_mode-\n')

    main_rx()
    
    
# def NT(tx_file_buffer):
def NT():

    print('\n-NT_mode-\n')

    # main_nt(tx_file_buffer)
    main_nw()


def run():

    while GPIO.input(ON_OFF_SWITCH):
        print("\n-Running-\n")
        
        if (GPIO.input(NW_SWITCH)):

            # NT(files)
            GPIO.output(NW_LED, GPIO.HIGH)
            NT()
            
        elif GPIO.input(TX_RX_SWITCH):
            
            GPIO.output(TX_LED, GPIO.HIGH)
            TX(files[0])

            
        else:

            LAST_PACKET = RX()
            GPIO.output(TX_LED, GPIO.HIGH)



def end():
    # Closing
    print("\n-Closing-\n")

    if LAST_PACKET != 0:

        import compression2 as comp

        c = comp.LZWCompressor()
        c.uncompressFromFile('RXfile_A.txt', 'RXfile_A.txt')
        
    GPIO.remove_event_detect(TX_RX_SWITCH)
    GPIO.remove_event_detect(NW_SWITCH)
    # GPIO.cleanup()
    

def on_off():

    print("\n-ON/OFF-\n")

    if (GPIO.input(ON_OFF_SWITCH)):

        run()
            
    else:
        
        end()
        
    
def main(argv):

    INIT = initPorts(INIT)

    if not GPIO.input(ON_OFF_SWITCH):        

        files = loadFiles()

    GPIO.cleanup() # Sure this here???

        
if __name__ == "__main__":

    # INIT = True
    
    while(True):
        main(sys.argv)

