
# struct header{
#   unsigned char signature;
#   unsigned char type : 2; // The : 4 means that we are just going to use two bits of the 4 bytes reserved
# // Si podemos usar el ACK de la librería y decimos que un NACK es un ack con payload podemos hacer de esta variable un bool (un bit)
#   unsigned int id; // Is it enough with 4B to set the IDs of the packets (2^32) Maybe, it would be enough with an unsigned short
#   unsigned char padding : 1; // The : 1 means that we are just going to use one bit of the 4 bytes reserved
# };

ID_length = 32

def string2bits(s=''):
    return [bin(ord(x))[2:].zfill(7) for x in s]

def bits2string(b=None):
    return ''.join([chr(int(x, 2)) for x in b])

def get_bin(x, n=0):
    """
    Get the binary representation of x.

    Parameters
    ----------
    x : int
    n : int
        Minimum number of digits. If x needs less digits in binary, the rest
        is filled with zeros.

    Returns
    -------
    str
    """
    return format(x, 'b').zfill(n)

class Header:

    def __init__(self,signature,typ,ID,padding):
        self.signature = signature                # A-Team signature predefined ## ''.join(format(ord(x), 'b') for x in 'a')
        self.typ = typ # ''.join(format(ord(x), 'b') for x in '3')[-2:] ## ID will be 3='11', 2='10', 1='01', 0='00' 
        self.ID = ID                      
        self.padding = padding

    def __str__(self):
        h = []
        byte_length = 8
        
        head = string2bits(self.signature)[0] + string2bits(self.typ)[0][-2:] + get_bin(self.ID,ID_length) + string2bits(self.padding)[0][-1:]

        print(head)
        
        for i in range(0,6):
            byte_start = byte_length*i
            h.append(head[byte_start:byte_start+byte_length-1])

        print(h)
        
        return bits2string(h)

    # def header2bin(self):
        
    

class Packet:

    def __init__(self, header, payload):
        self.header = header
        self.payload = header

    
# class ACK(Packet):

    
