def rebuildData(string, id):

    file_len = 10000 #Size of the file in bytes
    chunk_len = 30 #Size of the chunk in bytes

    ## We have a list of zeros in all positions that have not been received that packet id.
    ## Also we have a list of zeros in all the position which packets have not been already
    ## written into the file. This is in case we receive packet 5, but packet 4 has not
    ## arrived yet.
    ids_received = [0]*round((file_len/chunk_len)+1)
    ids_writen = [0]*round((file_len/chunk_len)+1)
    ## I don't understand the concept of these variables.

    
    ## Check if the 'id' has been registered yet (repeated packets).
    ## If not: I register it; If yes: I ignore it.
    ##
    ## CheckRepeatedIDS(id) --> TRUE if everything OK, FALSE if 'id' already exists.
    if CheckRepeatedIDS(id, ids_received)==True:
        ids_received.insert(id, id)


    ## Check if the previous ids have been writen into the file (check "consecutivity").
    for t in range(0,id):
        if (ids_received[t]!=0 or id==0) and (ids_writen[t]==0 or id==0):
            writeFile(string)
            ids_writen.insert(id, id)
            ## Añades la variable "String" al fichero... Pero se hace cada vez que recibes un paquete?
        else:
            ## Guardar el string número 'id' para escribirlo después



























