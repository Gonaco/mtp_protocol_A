
# from lib_nrf24 import NRF24

byte_length = 8
signature_length = byte_length
ID_length = 32
typ_length = 2
padding_length = 1

SYNC = 0
ACK = 1
NACK = 2
FRAME = 3

A_TEAM_SIGN = 97                # The ASCII code of 'a'

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
    
    def __init__(self, header=Header(), payload=''):
        self.header = header
        self.payload = payload

    def __str__(self):
        return self.header.__str__()+self.payload.__str__()

    def getPayload(self):
        ret = ""
        for i in range(0, length(self.payload), 1):
            ret = ret + chr(self.payload[i])
        return ret
    
    def packet2byt(self):
        payload_byt = string2bits(self.payload.__str__())
        payload_bit = ''
        for i in range(0,len(payload_byt)):
            payload_bit = payload_bit + payload_byt[i]
        return self.header.header2byt()+payload_bit

    def strMssg2Pckt(self, message_string):
        self.header.extractHeader(message_string)
        self.payload = message_string[6:]

    # def send(self,transceiver):
    #     transceiver.write(self.__str__())
    # Simple things, please

    
class ACK(Packet):

    # Class Constructor
    
    def __init__(self, ID, payload):
        header = Header(97,ACK,ID,0)
        Packet.__init__(self,header,payload)

class SYNC(Packet):

    # Class Constructor
    
    def __init__(self, ID, payload):
        header = Header(97,SYNC,ID,0)
        Packet.__init__(self,header,payload)    


class Frame(Packet):

    # Class Constructor
    
    def __init__(self, ID, padding, payload):
        header = Header(97,FRAME,ID,padding)
        Packet.__init__(self,header,payload)


class FrameSimple(Frame):

    # Class Constructor
    
    def __init__(self, ID):
        Frame.__init__(self,ID,1,ID.__str__())
