
# struct header{
#   unsigned char signature;
#   unsigned char type : 2; // The : 4 means that we are just going to use two bits of the 4 bytes reserved
# // Si podemos usar el ACK de la librería y decimos que un NACK es un ack con payload podemos hacer de esta variable un bool (un bit)
#   unsigned int id; // Is it enough with 4B to set the IDs of the packets (2^32) Maybe, it would be enough with an unsigned short
#   unsigned char padding : 1; // The : 1 means that we are just going to use one bit of the 4 bytes reserved
# };

class Header:
    signature = 'A'                # A-Team signature predefined
    typ = None
    ID = None
    padding = None
    

class Packet:
    header = None
    payload = None

    def setHeader(self):
        self.header = Header()
        
