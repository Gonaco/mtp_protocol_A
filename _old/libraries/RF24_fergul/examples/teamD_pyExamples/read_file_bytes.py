#Read file as array of chars
in_file = open("hola.txt", "rb")
total_data = []
data = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
in_file.close()
k=29

print(type(data))
print(len(data))
print(data)
paquetitos = []
length = len(data)-len(data)%k;
#print(data[0:k])
hola = range(0,len(data),k)
#print(hola)
#for i in hola:
    #print(i)
for i in hola:
    if (i+k)>len(data):
        paquetitos.append(data[i:])
        #print(data[i:])
    else:
        paquetitos.append(data[i:i+k])
        #print(data[i:k-1])
    print(paquetitos)

##########################################
# AQUÍ VA EL CODIGO DE FORMACIÓN DEL PAQUETE (CABECERA + CRC)
#
#
# FIN TX ---------------------------------
##########################################
##########################################
##########################################
# INICIO RX ------------------------------
# AQUÍ VA EL CODIGO DE DESENCRIPTACION:
# 1. COMPROVAR CRC
# 2. EXTRAER PAYLOAD DEL PAQUETE
#
##########################################

## IMPRIMIMOS EN HOLA2 LOS PAQUETITOS
out_file = open("hola2.txt", "wb") # open for [w]riting as [b]inary
for i in paquetitos:
    out_file.write(i)
out_file.close()









































































#print(type(total_data))
#print(len(total_data))
#print(total_data)
#print('element by element')
#for i in total_data:
#    print(i)


#print(data)
#lista_char = list(data);
#print(lista_char)

#convert to ascii (but expressed as an int)
#lista_ascii_int = [];
#for element in lista_char:
#    lista_ascii_int.append(ord(element))
#print(lista_ascii_int)

#print('los buenos')
#for element in lista_ascii_int:
#    print(bin(element))
#print('hasta aqui')
#convert to bytes
#lista_bytes = bytearray(lista_ascii_int);
#print(type(lista_bytes))
#print(len(lista_bytes))
#print(lista_bytes)

#import binascii
#print("eooooooo aqui!!! -----------------------------------------------")
#for i in lista_bytes:

#    print(binascii.hexlify(i))
#    print()


##TRABAJAR CON LISTA_BYTES

#bytes_alone = [lista_bytes[i:i+2] for i in range(0, len(data), 2)]




#out_file = open("hola2.txt", "wb") # open for [w]riting as [b]inary
#out_file.write(lista_bytes)
#out_file.close()
#print('end of experiment')
#print()
#print()

#print('experimento 2')
#in_file = open("hola.txt", "rb")
#data2 = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
#in_file.close()




#qwerty
#uiop
#zxcv bnm
#dfgh,ty
#wert, tyui
#ghj. hjk-
#qw123456poi
#áèíòú ñç
#<ºª!"·$%&/(=)(/¿*^¨