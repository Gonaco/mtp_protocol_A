import Net_main_functions as nw

ears, mouth = nw.setup()

timer = 1

# while True:
#     if (nw.listen(ears, timer)):
#         nw.passive(ears,mouth)
#     else:
#         print("Timeout")

while True:
    
    nw.active(ears,mouth)
    if (nw.listen(ears, timer)):
        print ("ACK received")

    else:
        print("Timeout")

# f = open("tx_file.txt", 'r')

# files = [f,f,f]

# nw.network_mode(ears,mouth,files)
