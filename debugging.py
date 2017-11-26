import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import spidev

GPIO.setmode(GPIO.BCM)

RF_CH = [0x00, 0x32]
BR = NRF24.BR_250KBPS
PA = NRF24.PA_MIN


def setup():
    # print("\n-setup-\n")

    pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]  # addresses for TX/RX channels

    GPIO.setup([0, 1, 17, 27], GPIO.OUT, initial=GPIO.LOW)

    ears = NRF24(GPIO, spidev.SpiDev())  # EARS
    mouth = NRF24(GPIO, spidev.SpiDev())  # MOUTH
    ears.begin(1, 27)  # Set spi-cs pin1, and rf24-CE pin 17
    mouth.begin(0, 17)  # Set spi-cs pin0, and rf24-CE pin 27

    ears.setRetries(15, 15)
    ears.setPayloadSize(32)
    ears.setChannel(RF_CH[0])
    mouth.setRetries(15, 15)
    mouth.setPayloadSize(32)
    mouth.setChannel(RF_CH[1])

    ears.setDataRate(BR)
    ears.setPALevel(PA)
    mouth.setDataRate(BR)
    mouth.setPALevel(PA)

    ears.setAutoAck(False)
    ears.enableDynamicPayloads()  # ears.setPayloadSize(32) for setting a fixed payload
    ears.enableAckPayload()
    mouth.setAutoAck(False)
    mouth.enableDynamicPayloads()
    mouth.enableAckPayload()

    mouth.openWritingPipe(pipes[0])
    ears.openReadingPipe(1, pipes[1])

    if not mouth.isPVariant():
        # If radio configures correctly, we confirmed a "plus" (ie "variant") nrf24l01+
        # Else print diagnostic stuff & exit.
        mouth.printDetails()
        # (or we could always just print details anyway, even on good setup, for debugging)
        print ("NRF24L01+ not found.")
        return

    if not ears.isPVariant():
        # If radio configures correctly, we confirmed a "plus" (ie "variant") nrf24l01+
        # Else print diagnostic stuff & exit.
        ears.printDetails()
        # (or we could always just print details anyway, even on good setup, for debugging)
        print ("NRF24L01+ not found.")
        return

    mouth.startListening()
    mouth.stopListening()

    mouth.printDetails()

    ears.startListening()
    # print('finish set up')
    return ears, mouth

setup()
GPIO.cleanup()

