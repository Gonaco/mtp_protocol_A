fichero1 = open("test1.txt", "rb")
data1 = fichero1.read()
fichero1.close()
size1 = len(data1)

# fichero2 = open("test2.txt", "rb")
# data2 = fichero2.read()
# fichero2.close()
# size2 = len(data2)

k=10
#print("Los datos son del tipo: ",type(data1))
#print("La cantidad total de datos es: ",len(data1))

######## SEPARACIÓN DE DATOS
seg1 = []
aux1 = []
#seg2 = []
# aux2 = []

for i in range(0,size1,k):
    if (i+k)>size1:
        seg1.append(data1[i:])
        #print(segmento) # ESTO IMPRIME AL FINAL
    else:
        seg1.append(data1[i:i+k])
        #print(segmento) # ESTO ACUMULA IMPRESIONES

    if (seg1 == aux1):
        print("Los paquetes son iguales")
    else:
        print("Los paquetes no son iguales")

    aux1 = seg1

print("El programa ha terminado")


# for j in range(0, size2, k):
#     if (i + k) > size2:
#         seg2.append(data2[j:])
#         # print(segmento) # ESTO IMPRIME AL FINAL
#     else:
#         seg2.append(data2[j:j + k])
#         # print(segmento) # ESTO ACUMULA IMPRESIONES

# This function is used in order to add redundancy to the system, so if one of the Ethernet interfaces has a problem,
# there are others that will work. Besides while all the interfaces are running the overall communications capacity will
# be computed as the sum of the individual ones (increasing bandwidth) and therefore upgrading the velocity of the system.
#
# Lets assume there are two different Ethernet interfaces connected between two switches, both with a bit rate of 100Mbps.
# When the switches agree to create a link aggregation, both Ethernet interfaces will combine an create a virtual link
# that will have a capacity of 200Mbps. If the LACP is not enable in both terminals, a local LAG (Link Aggregation Group)
# will try to transmits the packets through a single interface and the communication will fail, unless LACP is enable and
# both terminals are configured with LAG parameters.