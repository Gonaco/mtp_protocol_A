def splitData(PacketID, archivo):

    print("\n-splitData-\n") ##Debbuging issues.
	

    file_len = 10000 #Size of the file in bytes
    chunk_len = 30 #Size of the chunk in bytes

    archivo.seek(PacketID*chunk_len) #It moves the pointer to the starting point of the chunk number 'nPacket'
    chunk = archivo.read(chunk_len) #It reads 'cunk_len' bytes from the previous pointer


    if PacketID>round((file_len/chunk_len)+1):
        print("That packet does not exist. EOF reached.")
	

    return chunk


## Ejemplo de funcionamiento ##
## nPacket = 24
## chunk = splitData(nPacket)
## print(chunk)







