import packetManagement as pm
import math
import compression

archivo = open('Loremipsum.txt', 'rb')

##file_len = len(archivo.read())
chunk_len = 30


################
### COMPRESS ###
################
list_to_send = pm.splitData('Loremipsum.txt', chunk_len)
packets = len(list_to_send)

print("list_to_send: " + str(list_to_send))



##################
### UNCOMPRESS ###
##################
last_w_id = -1
storedFrames = {"-2N" : "DEFAULT"}
team = 'A'
global_string = None
for p_id in range(0, int(packets)):
    chunk = list_to_send[p_id]
    ##print("chunk: " + chunk)
    global_string, storedFrames, last_w_id = pm.rebuildData(p_id, chunk, last_w_id, storedFrames, team, global_string)

