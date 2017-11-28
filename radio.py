import time
import socket
import select
import random

class Radio(object):

    def __init__(self, pipes, rx, pins, teamID, UDP=False):
        # ### Radio interfaces ####
        self.UDP = UDP
        self.teamID = teamID
        if UDP:
            self.UDP_IP = "127.0.0.1"
            if rx:
                self.rx_UPD_port = 5005 + teamID

            else:
                self.tx_UDP_ports = [5005 + i for i in range(4)]
                self.tx_UDP_ports.remove(5005 + teamID)
                self.tx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            # from nrf24 import NRF24
            # import RPi.GPIO as GPIO
            import spidev
            import RPi.GPIO as GPIO
            from lib_nrf24 import NRF24

            GPIO.setmode(GPIO.BCM)


            # ### Network parameters ####
            RF_CH = [0x50]  # UL & DL channels
            PWR_LVL = NRF24.PA_MIN  # Transceiver output (HIGH = -6 dBm + 20 dB)
            BRATE = NRF24.BR_250KBPS  # 250 kbps bit rate
            PLOAD_SIZE = 32
            # self.radio = NRF24()

            self.pipes = pipes

            # if rx:
            #     self.radio.begin(0, 1, 24, 18)
            # else:
            #     self.radio.begin(0, 0, 25, 18)

            # self.radio.setPayloadSize(PLOAD_SIZE)
            # self.radio.setChannel(RF_CH[0])
            # self.radio.setDataRate(NRF24.BR_250KBPS)
            # self.radio.setPALevel(NRF24.PA_MIN)
            # self.radio.setAutoAck(False)
            # self.radio.enableDynamicPayloads()
            # self.radio.setCRCLength(NRF24.CRC_8)

            # # Open the writing and reading pipe
            # if rx:
            #     self.radio.openReadingPipe(1, self.pipes)
            # else:
            #     self.radio.openWritingPipe(self.pipes)

            # self.radio.printDetails()
            # print ("----------------------------------------")

            
            self.radio = NRF24(GPIO, spidev.SpiDev())
            # self.radio.begin(1, 27)


            GPIO.setup(pins[1], GPIO.OUT, initial=GPIO.LOW)
            self.radio.begin(pins[0],pins[1])
            
            time.sleep(1)

            # self.radio.setRetries(15, 15)
            self.radio.setPayloadSize(PLOAD_SIZE)
            self.radio.setChannel(RF_CH[0])
            
            self.radio.setDataRate(BRATE)
            self.radio.setPALevel(PWR_LVL)
            self.radio.setCRCLength(NRF24.CRC_8)

            self.radio.setAutoAck(False)
            self.radio.enableDynamicPayloads()
            self.radio.enableAckPayload()
            
            # self.radio.openWritingPipe(pipes[0])
            # Open the writing and reading pipe
            if rx:
                self.radio.openReadingPipe(0, self.pipes)
            else:
                self.radio.openWritingPipe(self.pipes)
            
            if not self.radio.isPVariant():
                # If self.radio configures correctly, we confirmed a "plus" (ie "variant") nrf24l01+
                # Else print diagnostic stuff & exit.
                self.radio.printDetails()
                # (or we could always just print details anyway, even on good setup, for debugging)
                print ("NRF24L01+ not found.")
                return

            self.radio.printDetails()

            timeout = time.time() + 0.1

    # Returns 0 if timer passed and 1 if something received
    def read(self, timeOut):
        buf = []
        if self.UDP:
            rx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            rx_socket.bind((self.UDP_IP, self.rx_UPD_port))
            rx_socket.setblocking(0)

            # print("Reading from socket...")
            ready = select.select([rx_socket], [], [], timeOut)
            if len(ready[0]) > 0:
                data, _ = rx_socket.recvfrom(1024)
                data = [ord(byte) for byte in data]
                # print("Received packet of len {} with header {:08b}".format(len(data), data[0]))
                rx_socket.close()

                # Emulate error probability
                error = random.randint(0, 20)
                if error == 1:
                    return 0, None
                return 1, data
            else:
                rx_socket.close()
                return 0, None
        else:

            startTime = time.time()
            self.radio.startListening()
            # TODO: check if this is correct
            while (time.time() - startTime) < timeOut and not self.radio.available([0]):
                pass

            if not self.radio.available([0]):
                # Return 0 if timeout reached
                self.radio.stopListening()
                return 0, None
            else:
                # Read the buffer and return in if something arrived
                self.radio.read(buf, self.radio.getDynamicPayloadSize())
                print("\n-Receiving-\n")
                print(buf)
                self.radio.stopListening()
                return 1, buf

    def write(self, buf):
        print("Sending packet of len {} with header {:08b}".format(len(buf), buf[0]))
        if self.UDP:
            buf = [chr(item) for item in buf]
            for tx_port in self.tx_UDP_ports:
                self.tx_socket.sendto("".join(buf), (self.UDP_IP, tx_port))
        else:
            self.radio.stopListening()
            print("\n-Sending-\n")            
            print(buf)
            self.radio.write(buf)
