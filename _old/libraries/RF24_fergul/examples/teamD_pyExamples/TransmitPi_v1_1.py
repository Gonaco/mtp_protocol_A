try:
    import RPi.GPIO as GPIO
    from lib_nrf24 import NRF24
    import time
    import spidev

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.output(23,1)
    GPIO.output(24,1)

    pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

    radio = NRF24(GPIO, spidev.SpiDev())
    radio2 = NRF24(GPIO, spidev.SpiDev())
    radio.begin(0, 17)
    radio2.begin(1, 17)
    radio.setPayloadSize(32)
    radio.setChannel(0x60)
    radio2.setPayloadSize(32)
    radio2.setChannel(0x65)

    radio.setDataRate(NRF24.BR_2MBPS)
    radio.setPALevel(NRF24.PA_MIN)
    radio.setAutoAck(False)
    radio.enableDynamicPayloads()
    radio2.setDataRate(NRF24.BR_2MBPS)
    radio2.setPALevel(NRF24.PA_MIN)
    radio2.setAutoAck(False)
    radio2.enableDynamicPayloads()
##    radio.enableAckPayload()

    # radio.openReadingPipe(1, pipes[1])
    radio.openWritingPipe(pipes[1])
    radio.printDetails()
    print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
    radio2.openReadingPipe(0, pipes[0])
    radio2.printDetails()
    ack  =  []
    # radio.startListening()
    # message = list(input("Enter a message to send: "))

    infile = open("/boot/Quick/hola1.txt", "rb")
    totaldata=[]
    data = infile.read()
    infile.close()
    sizepayload = 31
    flag="A"
    flag_first=1
    flag_previous=""
    packets = []
    
    for i in range(0,len(data),sizepayload):
        if (i+sizepayload)>len(data):
            packets.append(data[i:])
        else:
            packets.append(data[i:i+sizepayload])
    
##    while(1):
    vtime=time.time()
    print(format(time.time()))
    for message in packets:
        radio.write(flag + message)
        flag_previous=flag
        flag_first=0
        if flag  == "A":
            flag = "B"
        else :
            if flag  == "B":
                flag = "C"
            else:
                if flag  == "C":
                    flag = "A"
        #print("We sent the message of {}".format(message))
        radio2.startListening()
        timeout = time.time() + 0.1
        while (1):
            if radio2.available(0):
                radio2.read(ack, radio2.getDynamicPayloadSize())
                #print (ack+ list("!!!!!!!!!!!!!!!!!!!!!!!!!!"))
                if((list("ACK") + list(flag))==ack):#flag_previous==chr(ack[3]) and len(ack)==4):
                    radio.write(flag_previous + message)
                else:
                    #print("ACK break!!!!!!!!!!")
                    break
            else:
                if(time.time() + 1/2000 > timeout):
                    #print("resending message!!!!!!!!!!")
                    radio.write(flag_previous + message)
                    timeout = time.time() + 0.1

    
    v2time=  time.time()-vtime               
    print(format(time.time()))
    print(v2time)






















       
    GPIO.output(23,0)
    GPIO.output(24,0)    
except KeyboardInterrupt:
    GPIO.cleanup()
