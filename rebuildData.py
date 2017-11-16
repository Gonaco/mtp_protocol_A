storedFrames = {-2 : "DEFAULT"} ##Inicializamos el diccionario.
last_w_id = -1

def rebuildData(p_id, string, last_w_id, storedFrames, filename):
    
    print ("\n-rebuildData-\n") ##Debbuging issues
    
    if (p_id == last_w_id + 1): ## El paquete recibido es el siguiente que tenemos que escribir
        
        writeFile(string, filename) ##Escribimos 'string' en 'filename'
        last_w_id = last_w_id + 1 ##Actualizamos el ID del último paquete escrito
        
        p_id = p_id + 1
        while storedFrames.has_key(p_id): ## Comprobamos si está el paquete p_id+1 y posteriores consecutivos en el diccionario
            string = storedFrames[p_id] ##Extraemos el 'string' número 'p_id'
            writeFile(string, filename) ##Escribimos 'string' en 'filename'
            del storedFrames[p_id] ##Eliminamos del diccionario el string que acabamos de escribir
            last_w_id = last_w_id + 1 ##Actualizamos el ID del último paquete escrito
            p_id = p_id + 1 ##Incrementamos el ID del paquete para ver en la siguiente iteración si está en el diccionario
        
    elif (p_id > last_w_id):
        ## El paquete recibido todavía no lo podemos escribir
        ## -> Lo añadimos en el diccionario
        storedFrames.update({p_id : string})
        
    ## Devolvemos el diccionario y el last_w_id actualizados
    return storedFrames, last_w_id    

 
