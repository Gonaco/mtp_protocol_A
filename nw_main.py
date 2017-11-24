import Net_main_functions as nw
import time

# ears, mouth = nw.setup()

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
    return
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

    mouth.write("abcdefghijklmnñopqrstuvwxyz")
    

# f = open("tx_file.txt", 'r')

# files = [f,f,f]

# nw.network_mode(ears,mouth,files)
