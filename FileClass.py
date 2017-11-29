PAYLOAD_SIZE = 31


class FileClass(object):
    # This should be an abstract Object

    def __init__(self, reader, path):

        self.bytes = []
        self.packets = []
        self.path = path
        self.send_ack = 0

        # If file is to send, counter is used to check if we have to send the next packet
        # If file is to receive, counter is used to check if we should write the next chunk
        self.counter = 0

        self.finished = False

        if reader:
            print("Reading from file: {}".format(path))
            with open(path, 'rb') as f:
                byte = f.read(1)
                while byte != '':
                    self.bytes.append(byte)
                    byte = f.read(1)

                rest = len(self.bytes)

                aux = []
                for i in range(len(self.bytes)):
                    aux.append(ord(self.bytes[i]))
                    if len(aux) == PAYLOAD_SIZE or len(aux) == rest:
                        rest -= len(aux)
                        self.packets.append(aux)
                        aux = []
        else:
            pass
            with open(path, 'wb') as f:
                print("Created file in path: {}".format(path))

    # Sender methods
    def getNextPayload(self):
        if self.counter == len(self.packets):
            self.finished = True
            print("Sending last packet!")
            return [99], 0b11111
        packet_str = [chr(item) for item in self.packets[self.counter]]
        print("Getting packet in position {}: [{}]".format(self.counter, "".join(packet_str)))
        return self.packets[self.counter], self.counter

    def receivedACK(self):
        self.counter += 1
        print("Now counter is equal to: {}".format(self.counter))

    # Receiver methods
    def writePayload(self, buf, packet_counter):
        if packet_counter == 0b11111:
            print("No more packets to receive!")
            self.finished = True
            return
        print("Writting to file: self counter: {}, received counter: {}".format(self.counter, packet_counter))
        # If buf contains a list of ints (0-255), do char() and save to file one by one
        if packet_counter == self.counter:
            with open(self.path, 'ab') as f:
                for b in buf:
                    f.write(chr(b))
            self.counter += 1
            print("Now writing counter is equal to: {}".format(self.counter))
        self.send_ack = 1
