def splitData(PacketID, archivo):

    print("\n-splitData-\n") ##Debbuging issues.
	
    ## Modo normal:	
    ## Itzi comprime el archivo y nos lo manda para que "recortemos" el chunk número 'PacketID' y meterlo como payload del paquete.
    ##
    ## Network Mode:
    ## Nacho me pasa el archivo ABIERTO y el ID del paquete que necesite. Yo le devuelvo el chunk (es un string) para formar el payload.

	
    file_len = len(archivo.read()) #Size of the file in bytes
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







