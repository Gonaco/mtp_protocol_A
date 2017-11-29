
from lib_nrf24 import NRF24

from threading import Thread

byte_length = 8
# signature_length = byte_length
ID_length = 16
typ_length = 2
end_length = 1

SYNC_TYPE = 0
ACK_TYPE = 1
NACK_TYPE = 2
FRAME = 3

HEADER_BYTES_LENGTH = 3
FRAME_PAYLOAD_BYTES_LENGTH = 29

# A_TEAM_SIGN = 97                # The ASCII code of 'a'


def subSend(r,s):
    r.write(s)

    
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
    
    def __init__(self,typ=SYNC_TYPE,ID=0,end=0):

        # self.signature = signature                # A-Team signature predefined ## ''.join(format(ord(x), 'b') for x in 'a')
        self.typ = typ # ''.join(format(ord(x), 'b') for x in '3')[-2:] ## ID will be 3='11', 2='10', 1='01', 0='00' 
        self.ID = ID                      
        self.end = end

    # Class2String

    def __str__(self):

        h = []
        
        bin_head = get_bin(self.ID,ID_length) + get_bin(self.typ,typ_length) + get_bin(self.end,end_length)+'00000'
        
        for i in range(0,HEADER_BYTES_LENGTH):
            byte_start = byte_length*i
            h.append(bin_head[byte_start:byte_start+byte_length])

        return bits2string(h) 

    def getTyp(self):
        return self.typ

    def getID(self):
        return self.ID

    def getEnd(self):
        return self.end

    # Class2Binarycode split in Bytes

    def header2byt(self):
        return get_bin(self.ID,ID_length) + get_bin(self.typ,typ_length) + get_bin(self.end,end_length)+'00000'

    # Extract the Header from a message

    def extractHeader(self,rcv_str):

        # print(rcv_str)

        head = string2bits(rcv_str[:HEADER_BYTES_LENGTH])

        # self.signature = int(head[0], 2)
        # self.typ = int(head[1][:2], 2)
        # self.ID = int(head[1][2:]+head[2]+head[3]+head[4]+head[5][:2], 2)
        # self.end = int(head[5][2], 2)
        self.ID = int(head[0]+head[1],2)
        self.typ = int(head[2][:2], 2)
        self.end = int(head[2][2],2)
        # print(self.ID)

        
class Packet:

    # Class Constructor
    
    def __init__(self, header=Header(), payload=''):
        self.header = header
        self.payload = payload

    def __str__(self):
        return self.header.__str__()+self.payload.__str__()

    def getPayload(self):
        # ret = ""
        # for i in range(0, len(self.payload), 1):
        #     ret = ret + self.payload[i]
        return self.payload

    def getTyp(self):
        return self.header.getTyp()

    def getID(self):
        return self.header.getID()

    def getEnd(self):
        return self.header.getEnd()
    
    def packet2byt(self):
        payload_byt = string2bits(self.payload.__str__())
        payload_bit = ''
        for i in range(0,len(payload_byt)):
            payload_bit = payload_bit + payload_byt[i]
        return self.header.header2byt()+payload_bit

    def mssg2Pckt(self, message_bin):
        mssg_string = ""

        # print(message_bin)
        
        for i in range(0,len(message_bin),1):
            mssg_string = mssg_string + chr(message_bin[i])

        # print(mssg_string)
            
        self.header.extractHeader(mssg_string)
        self.payload = mssg_string[HEADER_BYTES_LENGTH:]

        # print(self.getID())
        
    # def send(self,transceiver):
    #     transceiver.write(self.__str__())

    
class ACK(Packet):

    # Class Constructor
    
    def __init__(self, ID, end): # TO Change No Payload and Test if it sends with no payload
        header = Header(ACK_TYPE,ID,end)
        Packet.__init__(self,header,'')

class NACK(Packet):

    # Class Constructor
    
    def __init__(self, ID, payload):
        header = Header(NACK_TYPE,ID,0)
        Packet.__init__(self,header,payload)


class SYNC(Packet):

    # Class Constructor
    
    def __init__(self, ID):
        header = Header(SYNC_TYPE,ID,0)
        Packet.__init__(self,header,'')    


class Frame(Packet):

    # Class Constructor
    
    def __init__(self, ID, end, payload):
        header = Header(FRAME,ID,end)
        Packet.__init__(self,header,payload)

        
def sendSYNC(ID, radio):

    # print("\n-sendSYNC-\n")
    sync = SYNC(ID)

    # print(sync)
    # radio.write(sync.__str__())
    send_thrd = Thread (target = subSend, args = (radio,sync.__str__()))
    send_thrd.start()

def sendACK(ID, end, radio):

    # print("\n-sendACK-\n")
    ack = ACK(ID, end)

    # print(ack)
    # radio.write(ack.__str__())
    send_thrd = Thread (target = subSend, args = (radio,ack.__str__()))
    send_thrd.start()

def sendNACK(ID, lost_IDs_array, radio):

    # print("\n-sendNACK-\n")
    
    payload = ""
    overload = []
    
    for i in range(0, len(lost_IDs_array)):
        
        if len(payload + str(lost_IDs_array[i]) + ",") <= FRAME_PAYLOAD_BYTES_LENGTH:
            payload = payload + str(lost_IDs_array[i]) + ","
        else:
            # print("Overload")
            overload = lost_IDs_array[i+1:]
            break
        
    nack = NACK(ID,payload)

   # print(nack.getTyp())
    #print(nack.getID())
    # print(nack.getPayload())
    #print(nack)

    # radio.write(nack.__str__())
    send_thrd = Thread (target = subSend, args = (radio,nack.__str__()))
    send_thrd.start()

    return overload


# NETWORK MODE

NETWORK_TYPE_LENGTH = 1
NETWORK_X_LENGTH = 2                  # The length of the Transmitter/Receiver/Next parameter
NETWORK_POS_LENGTH = 5
NETWORK_ACK_LENGTH = 1

N_ACK_OK = 1

DATA_FRAME_TYPE = 1
CONTROL_FRAME_TYPE = 0

A_TEAM = 0
B_TEAM = 1
C_TEAM = 2
D_TEAM = 3


class DataFrame:

    # Class Constructor
    
    def __init__(self, rx=B_TEAM, pos=0, payload=''):
        self.typ = DATA_FRAME_TYPE
        self.rx = rx
        self.pos = pos
        self.payload = payload

    def __str__(self):
        h = []
        
        bin_head = get_bin(self.typ, NETWORK_TYPE_LENGTH) + get_bin(self.rx, NETWORK_X_LENGTH) + get_bin(self.pos, NETWORK_POS_LENGTH)
        
        h.append(bin_head)

        header = bits2string(h)
        
        return header + self.payload

    def getTyp(self):
        return self.typ

    def getRx(self):
        return self.rx
    
    def getPos(self):
        return self.pos

    def getPayload(self):
        # ret = ""
        # for i in range(0, len(self.payload), 1):
        #     ret = ret + self.payload[i]
        return self.payload
    
    def d2byt(self):
        h = []

        h.append(get_bin(self.typ, NETWORK_TYPE_LENGTH) + get_bin(self.rx, NETWORK_X_LENGTH) + get_bin(self.pos, NETWORK_POS_LENGTH))
        
        return h + string2bits(self.payload)

    def mssg2Pckt(self, message_bin):
        mssg_string = ""
        
        for i in range(0,len(message_bin),1):
            mssg_string = mssg_string + chr(message_bin[i])

        head = string2bits(mssg_string[0])
        
        self.typ = int(head[0][:1],2)
        self.rx = int(head[0][1:3], 2)
        self.pos = int(head[0][3:],2)

        self.payload = mssg_string[1:]

        if self.typ != DATA_FRAME_TYPE:
            return False
        
        return True
        
    # def send(self,transceiver):
    #     transceiver.write(self.__str__())


class ControlFrame:

    # Class Constructor

    def __init__(self, nxt=B_TEAM, ack1=0, ack2=0, ack3=0):
        self.typ = CONTROL_FRAME_TYPE
        self.tx = A_TEAM
        self.nxt = nxt
        self.ack1 = ack1 
        self.ack2 = ack2
        self.ack3 = ack3

    def __str__(self):
        h = []
        
        bin_head = get_bin(self.typ, NETWORK_TYPE_LENGTH) + get_bin(self.tx, NETWORK_X_LENGTH) + get_bin(self.nxt,NETWORK_X_LENGTH) + get_bin(self.ack1,NETWORK_ACK_LENGTH) + get_bin(self.ack2,NETWORK_ACK_LENGTH) + get_bin(self.ack3,NETWORK_ACK_LENGTH)
        
        h.append(bin_head)

        return bits2string(h)

    def getTyp(self):
        return self.typ

    def getTx(self):
        return self.tx

    def getNxt(self):
        return self.nxt
    
    def getAck1(self):
        return self.ack1

    def getAck2(self):
        return self.ack2

    def getAck3(self):
        return self.ack3
        
    def c2byt(self):
        return get_bin(self.typ, NETWORK_TYPE_LENGTH) + get_bin(self.tx, NETWORK_X_LENGTH) + get_bin(self.nxt,NETWORK_X_LENGTH) + get_bin(self.ack1,NETWORK_ACK_LENGTH) + get_bin(self.ack2,NETWORK_ACK_LENGTH) + get_bin(self.ack3,NETWORK_ACK_LENGTH)

    def mssg2Pckt(self, message_bin):
        mssg_string = ""
        
        for i in range(0,len(message_bin),1):
            mssg_string = mssg_string + chr(message_bin[i])

        head = string2bits(mssg_string[0])
        
        self.typ = int(head[0][0],2)
        self.tx = int(head[0][1:3],2)
        self.nxt = int(head[0][3:5],2)
        self.ack1 = int(head[0][5],2)
        self.ack2 = int(head[0][6],2)
        self.ack3 = int(head[0][7],2)
        
        # self.payload = mssg_string[1:]

        if self.typ != CONTROL_FRAME_TYPE:
            return False

        return True
