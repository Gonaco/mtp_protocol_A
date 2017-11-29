import packetManagement as pm
import math
import compression

def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()
def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print( "Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print( "Toc: start time not set")



tx_filename = 'Loremipsum.txt'
#tx_filename = 'input - copia.txt'

##file_len = len(archivo.read())
chunk_len = 30


################
### COMPRESS ###
################
tic()

list_to_send = pm.splitData(tx_filename, chunk_len)
packets = len(list_to_send)

toc()

#print("list_to_send: " + str(list_to_send))



##################
### UNCOMPRESS ###
##################
last_w_id = -1
storedFrames = {"-2N" : "DEFAULT"}
team = 'A'
global_string = None
current_byte = 0
total_string = ''

tic()

for p_id in range(0, int(packets)):
    chunk = list_to_send[p_id]
    total_string, last_w_id, storedFrames, current_byte = pm.rebuildDataComp(p_id, chunk, last_w_id, storedFrames, team, total_string, packets, current_byte)

toc()