dict = {-2 : "DEFAULT"}
last_w_id = -1

def rebuildData(id, string, last_w_id, dict, filename):
    
    if (id == last_w_id + 1):
        ## El paquete recibido es el siguiente que tenemos que escribir
        writeFile(string, filename)
        last_w_id = last_w_id + 1
        ## Comprobamos si hay el paquete id+1 y posteriores en el diccionario
        id = id + 1
        while dict.has_key(id):
            string = dict[id]
            writeFile(string, filename)
            del dict[id]
            last_w_id = last_w_id + 1
            id = id + 1
        
    elif (id > last_w_id):
        ## El paquete recibido es posterior al que tendriamos que escribir
        ## -> Lo añadimos en el diccionario
        dict.update({id : string})
        
    ## Devolvemos el diccionario y la last_w_id
    return dict, last_w_id    

 
