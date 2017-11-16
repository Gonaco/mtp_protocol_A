storedFrames = {-2 : "DEFAULT"}
last_w_id = -1

def rebuildData(p_id, string, last_w_id, storedFrames, filename):
    
    print "\n-rebuildData-\n"
    
    if (p_id == last_w_id + 1):
        ## El paquete recibido es el siguiente que tenemos que escribir
        writeFile(string, filename)
        last_w_id = last_w_id + 1
        ## Comprobamos si hay el paquete id+1 y posteriores en el diccionario
        p_id = p_id + 1
        while storedFrames.has_key(id):
            string = storedFrames[p_id]
            writeFile(string, filename)
            del storedFrames[p_id]
            last_w_id = last_w_id + 1
            p_id = p_id + 1
        
    elif (p_id > last_w_id):
        ## El paquete recibido es posterior al que tendriamos que escribir
        ## -> Lo añadimos en el diccionario
        storedFrames.update({p_id : string})
        
    ## Devolvemos el diccionario y la last_w_id
    return storedFrames, last_w_id    

 
