MY_TEAM = 2
NEXT = 3
TX_ACK = [0, 0, 0, 0]
RX_ACK = [0, 0, 0, 0]
PAYLOAD_SIZE = 32
HEADER_SIZE = 1


def printBinary(byte):
    print('{:08b}'.format(byte))


def binaryStrToInt(binaryStr):
    num = 0
    for i in range(len(binaryStr)):
        num += int(binaryStr[len(binaryStr) - i - 1]) << i
    return num


def set_bit(input_byte, bit, value):
    if value == 1:
        return input_byte | (1 << bit)
    elif value == 0:
        return input_byte & ~(1 << bit)
    else:
        raise Exception("Value must be 1 or 0")


def getSender(header):
    header = '{:08b}'.format(header)
    return binaryStrToInt(header[1:3])


def generateControl(myteam, next_team, saving_files, networkSize):
    header = int((myteam << 5) + (next_team << 3))
    count = 0
    for i in range(networkSize):
        if i != myteam:
            header += saving_files[i].send_ack << 2 - count
            count += 1
    return [header]


# Generate control packet
def generateDataPacket(payload, rx_id, numPacket):
    header = (rx_id << 5) + numPacket
    # The first bit is 1 in data header
    header = [set_bit(header, 7, 1)]
    frameData = header + payload
    return frameData


def isControl(buf, teamID, networkSize):
    header = buf[0]
    header = '{:08b}'.format(header)
    packet_type = int(header[0])
    if packet_type != 0:
        return packet_type, None, None, None
    sender = binaryStrToInt(header[1:3])
    next_sender = binaryStrToInt(header[3:5])

    print("Acks are: {}".format(header[5:8]))
    # ACKs start at bit 5
    count = 5
    acks = [0, 0, 0, 0]
    for i in range(networkSize):
        if i != sender:
            acks[i] = int(header[count])
            count += 1
    ack = acks[teamID]
    print("ACKS: {}".format(acks))
    return packet_type, sender, ack, next_sender


def isData(buf, teamID):
    # 1 - 2 x Rx - 5 x POS - 29 x DATA
    # print("Checking if data...")
    header = buf[0]
    header = '{:08b}'.format(header)
    packet_type = int(header[0])
    receiver = binaryStrToInt(header[1:3])
    # print("The receiver is {} and I am {}".format(receiver, teamID))
    if packet_type != 1 or receiver != teamID:
        return None, None
    packet_counter = binaryStrToInt(header[3:8])
    payload = buf[1:]
    return payload, packet_counter
