import math
## ADDED AT RECENT REVIEW TO INCLUDE COMPRESSION
import compression2

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

##This is initialized by Carlos:
##storedFrames = {"-2N" : "DEFAULT"} ##Inicializamos el diccionario.

USING_COMPRESSION = True

## DISCLAIMER
# In network mode, we will need a last_w_id diferent for each team (!)
# Each last_w_id must be initialized at -1
# The dictionary must be created outside the function, initialised as shown on this file
# Team must be an string with the letter of the team in capital letter ("A", "B", "C", or "D")
def rebuildData(p_id, string, last_w_id, storedFrames, team):
    # print ("\n-rebuildData-\n")  ##Debbuging issues

    filename = "RXfile_" + team
    if (p_id == last_w_id + 1):  # The received packet is the one we should write.

        writeFile(string, filename, p_id)  # We write 'string' in 'filename'
        last_w_id = last_w_id + 1  # Update the last writen packet ID

        p_id = p_id + 1
        while storedFrames.has_key(str(
                p_id) + team):  # We check if the packet p_id+1 and the following consecutive ones are in the dictionary.
            string = storedFrames[str(p_id) + team]  # We extract the 'string' number 'p_id'
            writeFile(string, filename, p_id)  # We write 'string' in 'filename'
            del storedFrames[str(p_id) + team]  # Remove from the dictionary the string we have just writen
            last_w_id = last_w_id + 1  # Update the last writen packet ID
            p_id = p_id + 1  # Increase the packet ID to see in the next iteration if it is in diccionary

    elif (p_id > last_w_id):
        ## We cannot write the received packet yet.
        ## -> We add it to the dictionary
        storedFrames.update({str(p_id) + team: string})
        
    # print(storedFrames)
    ## We return the dictionary and the last writen id (updated versions)
    return storedFrames, last_w_id


## This function appends a given string to a file saved as filename (without including the .txt)
def writeFile(chunk, filename, p_id):
    # print('\n-writeFile-\n')
    ##finalFILE = open(filename + ".txt", 'a+')
    ##finalFILE.write(string)
    ##finalFILE.close()

    if p_id != 0:
        finalFILE = open(filename + '.txt', 'a+b')
        if chunk.__contains__('\n'):
            aux = chunk.split('\n')
            trozos = len(aux)

            for j in range(0, trozos - 1):
                finalFILE.write(aux[j] + '\n')
            finalFILE.write(aux[-1])
        else:
            finalFILE.write(chunk)
    else:
        finalFILE = open(filename + '.txt', 'wb')
        finalFILE.write(chunk)


## SPLIT DATA NOW COMPRESSES THE WHOLE FILE.        
def splitData(archivo, chunk_len):
    data_to_be_sent = archivo.read()
    if USING_COMPRESSION:
        tic()
        try:
            Compi_tx = compression2.DifferentialCompressor()
            data_ori = data_to_be_sent
            data_to_be_sent = Compi_tx.compress(data_to_be_sent)
            data_uncompressed = Compi_tx.uncompress(data_to_be_sent)
            if data_ori!=data_to_be_sent or (len(data_ori)/len(data_to_be_sent))<10:
                raise ValueError('A very specific bad thing happened.')
        except:
            Compi_tx = compression2.LZWCompressor()
            data_to_be_sent = Compi_tx.compress(data_to_be_sent)
        toc()

    ### splitting the data in packets
    list_to_send = []
    for ite in xrange(0,len(data_to_be_sent),chunk_len):
        list_to_send.append(data_to_be_sent[ite : ite + chunk_len])
    
    return list_to_send    
    
#    # print("\n-splitData-\n")  ##Debbuging issues.
#
#    file_len = len(archivo.read())  # Size of the file in bytes
#    # print('Size of the file in bytes: %s' % file_len)
#    ##chunk_len = 30  # Size of the chunk in bytes
#    # print('Size of the chunk in bytes: %s' % chunk_len)
#
#    aux = float(file_len) / chunk_len
#    packets = math.ceil(aux)
#    # print('Number of packets: %s' % packets)

#    lista = []
#    for i in range(0, int(packets)):
#        archivo.seek(i * chunk_len)
#        chunk = archivo.read(chunk_len)
#        lista.append(chunk)
#
#    ##archivo.seek(PacketID * chunk_len)  # It moves the pointer to the starting point of the chunk number 'nPacket'
#    ##chunk = archivo.read(chunk_len)  # It reads 'cunk_len' bytes from the previous pointer
#
#    ##if PacketID > packets):
#    ##    print("That packet does not exist. EOF reached.")
#
#    return lista
