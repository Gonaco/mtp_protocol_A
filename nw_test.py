import Net_main_functions as nw
import time

GPIO.setup([0,1,17,27], GPIO.OUT, initial=GPIO.LOW)
ears = NRF24(GPIO, spidev.SpiDev())  # EARS
ears.begin(1, 27)  # Set spi-cs pin1, and rf24-CE pin 17
ears.setRetries(15, 15)
ears.setPayloadSize(32)     # SURE?
ears.setChannel(RF_CH)
ears.setDataRate(BRATE)
ears.setPALevel(PWR_LVL)
ears.setAutoAck(False)
ears.enableDynamicPayloads()  # ears.setPayloadSize(32) for setting a fixed payload
ears.openReadingPipe(1, PIPES[0])
if not ears.isPVariant():
    # If radio configures correctly, we confirmed a "plus" (ie "variant") nrf24l01+
    # Else print diagnostic stuff & exit.
    ears.printDetails()
    # (or we could always just print details anyway, even on good setup, for debugging)
    print ("NRF24L01+ not found.")
    return
ears.printDetails()
ears.startListening()


while True:

    if ears.available([0]):
        print("Something received")

        recv_buffer = []
        ears.read(recv_buffer, ears.getDynamicPayloadSize())  # CHECK IT
        print(recv_buffer)
