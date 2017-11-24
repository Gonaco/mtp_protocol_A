import Net_main_functions as nw
import time

ears, mouth = nw.setup()

while True:

    if ears.available([0]):
        print("Something received")

        recv_buffer = []
        ears.read(recv_buffer, ears.getDynamicPayloadSize())  # CHECK IT
        print(recv_buffer)
