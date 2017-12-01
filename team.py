import radio
import packet
from FileClass import FileClass
import time
import os


class Team(object):

    def __init__(self, teamID, UDP=False, dilationFactor=1, networkSize=4):
        self.teamID = teamID
        self.nextPlayer = False
        self.waitingControl = True
        self.finishedCounter = 0

        self.networkSize = networkSize
        self.dilationFactor = dilationFactor
        self.tData = (0.005*3 + 0.005)*self.dilationFactor
        self.tACK = 0.04*self.dilationFactor

        self.savingFiles = [0]*self.networkSize
        self.senderFiles = [0]*self.networkSize
        for i in range(self.networkSize):
            if i != self.teamID:
                savingFilePath = os.path.join("/home/pi/mtp_protocol_A/savingFiles" + str(self.teamID), "team" + str(i), "received_file.txt")
                self.savingFiles[i] = FileClass(reader=False, path=savingFilePath)
                senderFolder = os.path.join("/home/pi/mtp_protocol_A/sendFiles" + str(self.teamID), "team" + str(i))
                senderFilePath = os.path.join(senderFolder, os.listdir(senderFolder)[0])
                self.senderFiles[i] = FileClass(reader=True, path=senderFilePath)

        self.pipeRX = [0xe7, 0xe7, 0xe7, 0xe7, 0xe7]
        self.pipeTX = [0xe7, 0xe7, 0xe7, 0xe7, 0xe7]

        # pinTX = int(raw_input("In which GPIO port did you connect the CE TX?"))
        # pinValTx = int(raw_input("Value to set CS TX?"))
        # pinRX = int(raw_input("In which GPIO port did you connect the CE RX?"))
        # pinValRx = int(raw_input("Value to set CS RX?"))

        pinTX = 27
        pinValTx = 1
        pinRX = 17
        pinValRx = 0
        

        self.radioTX = radio.Radio(self.pipeTX, rx=False, pins=[pinValTx, pinTX], teamID=self.teamID, UDP=UDP)
        self.radioRX = radio.Radio(self.pipeRX, rx=True, pins=[pinValRx, pinRX], teamID=self.teamID, UDP=UDP)

    def waitControl(self, timeout=None):
        startTime = time.time()
        timePassed = 0
        print(" +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- Waiting for control for {} seconds "
              "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-".format(timeout))
        while timeout > timePassed:
            result, packet_read = self.radioRX.read(timeout)
            if result == 0:
                print("Timeout finished, sending control")
                self.nextPlayer = True
                return 0, None
            else:
                typ, sender, ack, nextOne = packet.isControl(packet_read, self.teamID, self.networkSize)
                if typ == 0:
                    print("Received control")
                    if self.teamID == nextOne:
                        self.nextPlayer = True
                    if ack == 1:
                        self.senderFiles[sender].receivedACK()
                    return 1, packet_read
            timePassed = time.time() - startTime
        return 0, None

    def sendControl(self):
        print("Sending control...")
        controlPacket = packet.generateControl(self.teamID, (self.teamID + 1) % self.networkSize, self.savingFiles,
                                               self.networkSize)
        self.radioTX.write(controlPacket)
        for i in range(len(self.savingFiles)):
            if self.savingFiles[i] != 0:
                self.savingFiles[i].send_ack = 0
        return controlPacket

    def sender(self, waitOthersData):
        print("----------------- Now on sender mode waiting for {} seconds "
              "----------------------------------".format(waitOthersData))
        time.sleep(waitOthersData)
        # Wait for ack + send data
        sentPacket = self.sendControl()
        # When I send the control packet I am not longer the next one
        self.nextPlayer = False
        startTime = time.time()
        if self.waitACKs(self.tACK, sentPacket) == 1:
            print("Received ack, sending data")
            self.sendData()
        while time.time() - startTime < self.tData:
            pass

    def receiver(self, controlPacket):
        print("+++++++++++++++++++++++++ Now on receiver mode ++++++++++++++++++++++++++++++++++++++++++")
        # Send the ACK (same as control) but using a random timer beacuse of possible collisions
        startTime = time.time()
        time.sleep(float(self.teamID)/100 + 0.001*self.dilationFactor)
        self.radioTX.write(controlPacket)
        sender = packet.getSender(controlPacket[0])
        # Wait for all the ACK time (wait tACK)
        while time.time() - startTime < self.tACK - 0.00025*self.dilationFactor:
            pass
        self.receiveData(self.tData, sender)

    def waitACKs(self, timeout, sentPacket):
        startTime = time.time()
        ackCounter = 0
        timePassed = 0
        print("Now waiting for ACKs.")
        while True:
            print("Reading socket waiting for ACK...")
            result, packet_read = self.radioRX.read(timeout - timePassed)
            if result == 0:
                if ackCounter > 0:
                    print("ACK OK")
                    return 1
                print("ACK KO")
                return 0
            else:
                if packet_read[0] == sentPacket[0]:
                    ackCounter += 1
                    print("ACK received")
                else:
                    print("Not ACK, continue to listen until ACKs arrive or time expires.")
            timePassed = time.time() - startTime

    def sendData(self):
        print("Sending data...")
        for i in range(self.networkSize):
            if i != self.teamID:
                time.sleep(0.005*self.dilationFactor)
                payload, counter = self.senderFiles[i].getNextPayload()
                # Send the data if there is something to send
                if len(payload) > 0:
                    data = packet.generateDataPacket(payload, i, counter)
                    self.radioTX.write(data)

    def receiveData(self, timeout, sender):
        startTime = time.time()
        timePassed = 0
        myDataReceived = False
        while timeout > timePassed:
            result, packet_received = self.radioRX.read(timeout - timePassed)
            if result == 0:
                if myDataReceived:
                    print("Receiving time finished, data OK")
                else:
                    print("Receiving time finished, data not received!!")
            else:
                payload, packet_counter = packet.isData(packet_received, self.teamID)
                if payload is not None and packet_counter is not None:
                    myDataReceived = True
                    self.savingFiles[sender].writePayload(payload, packet_counter)
            timePassed = time.time() - startTime

    def checkFinished(self):
        finished = True
        for i in range(self.networkSize):
            if i != self.teamID:
                if not self.savingFiles[i].finished:
                    finished = False
                if not self.senderFiles[i].finished:
                    finished = False
        if finished:
            print("Everybody is finished!!!! counter is: {}".format(self.finishedCounter))
            self.finishedCounter += 1
            if self.finishedCounter > 4:
                return True
            else:
                print("Waiting in network for more rounds to make sure.")
        return False
