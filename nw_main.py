import Net_main_functions as nw
import time

ears, mouth = nw.setup()

timer = 1

# while True:
#     if (nw.listen(ears, timer)):
#         nw.passive(ears,mouth)
#     else:
#         print("Timeout")

while True:
    
    nw.active(ears,mouth)
    time.sleep(0.001)
    if (nw.listen(ears, timer)):
        print ("ACK received")

    else:
        print("Timeout")
    

# f = open("tx_file.txt", 'r')

# files = [f,f,f]

# nw.network_mode(ears,mouth,files)
