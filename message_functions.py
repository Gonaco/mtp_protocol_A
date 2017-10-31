
# struct header{
#   unsigned char signature;
#   unsigned char type : 2; // The : 4 means that we are just going to use two bits of the 4 bytes reserved
# // Si podemos usar el ACK de la librería y decimos que un NACK es un ack con payload podemos hacer de esta variable un bool (un bit)
#   unsigned int id; // Is it enough with 4B to set the IDs of the packets (2^32) Maybe, it would be enough with an unsigned short
#   unsigned char padding : 1; // The : 1 means that we are just going to use one bit of the 4 bytes reserved
# };

def string2bits(s=''):
    return [bin(ord(x))[2:].zfill(8) for x in s]

def bits2string(b=None):
    return ''.join([chr(int(x, 2)) for x in b])

class Header:
    signature = 'a'                # A-Team signature predefined ## ''.join(format(ord(x), 'b') for x in 'a')
    typ = None
    ID = 0                      # ''.join(format(ord(x), 'b') for x in '3')[-2:] ## ID will be 3='11', 2='10', 1='01', 0='00' 
    padding = False

    def header2bin(self):
        
    

class Packet:
    header = None
    payload = None

    def setHeader(self):
        self.header = Header()
        
