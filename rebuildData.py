##This is initialized by Carlos:
##storedFrames = {"-2N" : "DEFAULT"} ##Inicializamos el diccionario.
##last_w_id = -1


## DISCLAIMER
# In network mode, we will need a last_w_id diferent for each team (!)
# Each last_w_id must be initialized at -1
# The dictionary must be created outside the function, initialised as shown on this file
# Team must be an string with the letter of the team in capital letter ("A", "B", "C", or "D")
def rebuildData(p_id, string, last_w_id, storedFrames, team):
    
    print ("\n-rebuildData-\n") ##Debbuging issues
    
    filename = "RXfile_" + team
    if (p_id == last_w_id + 1): ## The received packet is the one we should write.

        writeFile(string, filename) ##We write 'string' in 'filename'
        last_w_id = last_w_id + 1 ##Update the last writen packet ID

        p_id = p_id + 1
        while storedFrames.has_key(str(p_id)+team): ## Comprobamos si est el paquete p_id+1 y posteriores consecutivos en el diccionario
            string = storedFrames[str(p_id)+team] ##Extraemos el 'string' nmero 'p_id'
            writeFile(string, filename) ##We write 'string' in 'filename'
            del storedFrames[str(p_id)+team] ##Remove from the dictionary the string we have just writen
            last_w_id = last_w_id + 1 ##Update the last writen packet ID
            p_id = p_id + 1 ##Increase the packet ID to see in the next iteration if it is in diccionary

    elif (p_id > last_w_id):
        ## We cannot write the received packet yet.
        ## -> We add it to the dictionary
        storedFrames.update({str(p_id)+team : string})
        
    ## We return the dictionary and the last writen id (updated versions)
    return storedFrames, last_w_id    

 
