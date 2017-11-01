
# struct header{
#   unsigned char signature;
#   unsigned char type : 2; // The : 4 means that we are just going to use two bits of the 4 bytes reserved
# // Si podemos usar el ACK de la librería y decimos que un NACK es un ack con payload podemos hacer de esta variable un bool (un bit)
#   unsigned int id; // Is it enough with 4B to set the IDs of the packets (2^32) Maybe, it would be enough with an unsigned short
#   unsigned char padding : 1; // The : 1 means that we are just going to use one bit of the 4 bytes reserved
# };

byte_length = 8
signature_length = byte_length
ID_length = 32
typ_length = 2
padding_length = 1

SYNC = 0
ACK = 1
NACK = 2
FRAME = 3

A_TEAM_SIGN = 97                # The ASCI code of 'a'

def string2bits(s=''):
    return [bin(ord(x))[2:].zfill(8) for x in s]

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

    # Class Constructor
    
    def __init__(self,signature=97,typ=SYNC,ID=0,padding=0):

        self.signature = signature                # A-Team signature predefined ## ''.join(format(ord(x), 'b') for x in 'a')
        self.typ = typ # ''.join(format(ord(x), 'b') for x in '3')[-2:] ## ID will be 3='11', 2='10', 1='01', 0='00' 
        self.ID = ID                      
        self.padding = padding

    # Class2String

    def __str__(self):

        h = []
        
        bin_head = get_bin(self.signature,signature_length) + get_bin(self.typ,typ_length) + get_bin(self.ID,ID_length) + get_bin(self.padding,padding_length)+'00000'
        
        for i in range(0,6):
            byte_start = byte_length*i
            h.append(bin_head[byte_start:byte_start+byte_length])

        return bits2string(h)


    # Class2Binarycode split in Bytes

    def header2byt(self):
        return get_bin(self.signature,signature_length) + get_bin(self.typ,typ_length) + get_bin(self.ID,ID_length) + get_bin(self.padding,padding_length)+'00000'

    # Extract the Header from a message

    def extractHeader(self,rcv_str):

        head = string2bits(rcv_str[0:7])

        self.signature = int(head[0], 2)
        self.typ = int(head[1][0:2], 2)
        self.ID = int(head[1][2:8]+head[2]+head[3]+head[4]+head[5][0:2], 2)
        self.padding = int(head[5][2], 2)
    

class Packet:

    # Class Constructor
    
    def __init__(self, header, payload):
        self.header = header
        self.payload = header

    
class ACK(Packet):

    # Class Constructor
    
    def __init__(self, ID, payload):
        header = Header(97,ACK,ID,0)
        Packet.__init__(self,header,payload)


class Frame(Packet):

    # Class Constructor
    
    def __init__(self, ID, padding, payload):
        header = Header(97,FRAME,ID,padding)
        Packet.__init__(self,header,payload)


class FrameSimple(Frame):

    # Class Constructor
    
    def __init__(self, ID):
        Frame.__init__(self,ID,1,ID)
