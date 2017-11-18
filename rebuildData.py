storedFrames = {"-2N" : "DEFAULT"} ##Inicializamos el diccionario.
last_w_id = -1


## DISCLAIMER
# In network mode, we will need a last_w_id diferent for each team (!)
# Each last_w_id must be initialized at -1
# The dictionary must be created outside the function, initialised as shown on this file
# Team must be an string with the letter of the team in capital letter ("A", "B", "C", or "D")
def rebuildData(p_id, string, last_w_id, storedFrames, team):
    
    print ("\n-rebuildData-\n") ##Debbuging issues
    
    filename = "RXfile_" + team
    if (p_id == last_w_id + 1): ## El paquete recibido es el siguiente que tenemos que escribir

        writeFile(string, filename) ##Escribimos 'string' en 'filename'
        last_w_id = last_w_id + 1 ##Actualizamos el ID del ltimo paquete escrito

        p_id = p_id + 1
        while storedFrames.has_key(str(p_id)+team): ## Comprobamos si est el paquete p_id+1 y posteriores consecutivos en el diccionario
            string = storedFrames[str(p_id)+team] ##Extraemos el 'string' nmero 'p_id'
            writeFile(string, filename) ##Escribimos 'string' en 'filename'
            del storedFrames[str(p_id)+team] ##Eliminamos del diccionario el string que acabamos de escribir
            last_w_id = last_w_id + 1 ##Actualizamos el ID del ltimo paquete escrito
            p_id = p_id + 1 ##Incrementamos el ID del paquete para ver en la siguiente iteracin si est en el diccionario

    elif (p_id > last_w_id):
        ## El paquete recibido todava no lo podemos escribir
        ## -> Lo aadimos en el diccionario
        storedFrames.update({str(p_id)+team : string})
        
    ## Devolvemos el diccionario y el last_w_id actualizados
    return storedFrames, last_w_id    

 
