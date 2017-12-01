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

TRANSCEIVERS = [0,1,17,27]

# FREE_PINS = [2,3,4,6,14,15,18,22,23,24,25] # [3,5,7,8,10,12,15,16,18,22,31] # IN ORDER TO SET THEM AS OUTPUT AND AVOID ERRORS

global LAST_PACKET
LAST_PACKET = 0

# global files

files = []

time_stamp = time.time()


def initPorts():

    print("\n-initPorts-\n")

    GPIO.setmode(GPIO.BCM)

    # INPUTS

    GPIO.setup(TX_RX_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    GPIO.setup(NW_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    GPIO.setup(ON_OFF_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.add_event_detect(ON_OFF_SWITCH, GPIO.BOTH)
    # GPIO.add_event_callback(ON_OFF_SWITCH, on_off)

    # GPIO.add_event_detect(ON_OFF_SWITCH, GPIO.RISING, callback=run)
    GPIO.add_event_detect(ON_OFF_SWITCH, GPIO.FALLING, callback=end)

    GPIO.setup(IRQS, GPIO.IN)

    # OUTPUTS

    # Tx/Rx

    GPIO.setup(TRANSCEIVERS, GPIO.OUT, initial=GPIO.LOW)

    # LEDS

    GPIO.setup(ON_OFF_LED, GPIO.OUT)
    GPIO.output(ON_OFF_LED, 0)
    
    GPIO.setup(NW_LED, GPIO.OUT)
    GPIO.output(NW_LED, 0)
    
    GPIO.setup(TX_LED, GPIO.OUT)
    GPIO.output(TX_LED, 0)

    # Just for being sure that there are no errors with the pins as input
    # GPIO.setup(FREE_PINS, GPIO.OUT)


    
# def loadFiles(argv):

    
def loadFiles():
    print("\n-loadFiles-\n")
    
    global files
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
            files.append(open("/home/pi/mtp_protocol_A/input_files/"+filename, 'rb'))


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

    return main_rx()
    
    
# def NT(tx_file_buffer):
def NT():

    print('\n-NT_mode-\n')

    # main_nt(tx_file_buffer)
    main_nw()


def run():

    GPIO.output(ON_OFF_LED, GPIO.HIGH)

    # while GPIO.input(ON_OFF_SWITCH):
    print("\n-Running-\n")

    if (GPIO.input(NW_SWITCH)):

        # NT(files)
        GPIO.output(NW_LED, GPIO.HIGH)
        NT()
        GPIO.output(NW_LED, GPIO.LOW)

    elif GPIO.input(TX_RX_SWITCH):

        GPIO.output(TX_LED, GPIO.HIGH)
        GPIO.output(ON_OFF_LED, GPIO.HIGH)            

        if files:
            TX(files[0])

        GPIO.output(TX_LED, GPIO.LOW)

    else:

        GPIO.output(TX_LED, GPIO.LOW)
        LAST_PACKET = RX()
        GPIO.output(TX_LED, GPIO.HIGH)
        if LAST_PACKET == 0:
            quit()



def end(channel):
    # Closing
    print("\n-Closing-\n")

    global time_stamp       # put in to debounce  
    time_now = time.time()  
    if (time_now - time_stamp)  >= 0.3 and not GPIO.input(ON_OFF_SWITCH):
        
        if LAST_PACKET != 0:

            import compression2 as comp

            c = comp.LZWCompressor()
            c.uncompressFromFile('RXfile_A.txt', 'RXfile_A.txt')
            
        GPIO.output(ON_OFF_LED, 0)    
            
        print("Quitting")
        quit()
    time_stamp = time_now  
        
    # GPIO.remove_event_detect(TX_RX_SWITCH)
    # GPIO.remove_event_detect(NW_SWITCH)
    # GPIO.cleanup()
    

def on_off():

    print("\n-ON/OFF-\n")

    if (GPIO.input(ON_OFF_SWITCH)):

        run()
            
    else:
        
        end()
        
    
def main(argv):

    loadFiles()
    if GPIO.input(ON_OFF_SWITCH):
        run()
        

    # loadFiles()
    # on_off()

        
if __name__ == "__main__":
    
    initPorts()
    
    while(True):
        main(sys.argv)
        
    GPIO.cleanup() # Sure this here???
