import math

##This is initialized by Carlos:
##storedFrames = {"-2N" : "DEFAULT"} ##Inicializamos el diccionario.


## DISCLAIMER
# In network mode, we will need a last_w_id diferent for each team (!)
# Each last_w_id must be initialized at -1
# The dictionary must be created outside the function, initialised as shown on this file
# Team must be an string with the letter of the team in capital letter ("A", "B", "C", or "D")
def rebuildData(p_id, string, last_w_id, storedFrames, team):
    print ("\n-rebuildData-\n")  ##Debbuging issues

    filename = "RXfile_" + team
    if (p_id == last_w_id + 1):  #The received packet is the one we should write.

        writeFile(string, filename)  #We write 'string' in 'filename'
        last_w_id = last_w_id + 1  #Update the last writen packet ID

        p_id = p_id + 1
        while storedFrames.has_key(str(p_id) + team):  #We check if the packet p_id+1 and the following consecutive ones are in the dictionary.
            string = storedFrames[str(p_id) + team]  #We extract the 'string' number 'p_id'
            writeFile(string, filename)  #We write 'string' in 'filename'
            del storedFrames[str(p_id) + team]  #Remove from the dictionary the string we have just writen
            last_w_id = last_w_id + 1  #Update the last writen packet ID
            p_id = p_id + 1  #Increase the packet ID to see in the next iteration if it is in diccionary

    elif (p_id > last_w_id):
        ## We cannot write the received packet yet.
        ## -> We add it to the dictionary
        storedFrames.update({str(p_id) + team: string})

    ## We return the dictionary and the last writen id (updated versions)
    return storedFrames, last_w_id


## This function appends a given string to a file saved as filename (without including the .txt)
def writeFile(chunk, filename):
    
    print('\n-writeFile-\n') #Debugging issues
    
    finalFILE = open(filename + ".txt", 'a+')
    ##finalFILE.write(string)
    ##finalFILE.close()

    if chunk.__contains__('\n'):
        aux = chunk.split('\n')
        trozos = len(aux)

        for j in range(0, trozos-1):
            finalFILE.write(aux[j] + '\n')
        finalFILE.write(aux[-1])
    else:
        finalFILE.write(chunk)


def splitData(archivo, chunk_len):

    print("\n-splitData-\n")  ##Debbuging issues.

    file_len = len(archivo.read())  # Size of the file in bytes
    ##chunk_len = 30  # Size of the chunk in bytes

    packets = math.ceil(file_len/chunk_len)

    lista = []
    for i in range(0, packets):
        lista.append(archivo.read(chunk_len))

    ##archivo.seek(PacketID * chunk_len)  # It moves the pointer to the starting point of the chunk number 'nPacket'
    ##chunk = archivo.read(chunk_len)  # It reads 'cunk_len' bytes from the previous pointer

    ##if PacketID > packets):
    ##    print("That packet does not exist. EOF reached.")

    return lista
