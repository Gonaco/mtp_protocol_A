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

    radio2.openWritingPipe(pipes[0])
    radio2.printDetails()
    print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
    radio.openReadingPipe(0, pipes[1])
    radio.printDetails()
    frame = []
    flag_frame=65
    char_flag=0
    str_frame=""
    str_frame1=""

    outputfile = open("/boot/Quick/hola1.txt", "wb")
    
    while(1):
        radio.startListening()
        str_frame=""
        if radio.available(0):
            radio.read(frame, radio.getDynamicPayloadSize())
            print(frame)
            print(frame[0])
            char_flag=frame[0]
            if(char_flag!=flag_frame):
                print("gggggggggggggggggggggggggggggggggggggggggggggggggggg")
                timeout=time.time()+2/10
                radio2.write(list("ACK") + list(chr(flag_frame)))
                radio.startListening()
                while(time.time()<timeout):
                    if radio.available(0):
                        radio.read(frame, radio.getDynamicPayloadSize())
                        char_flag=frame[0]
                        if(char_flag==flag_frame):
                            break
                    if(time.time()>(timeout-1/10)):
                        radio2.write(list("ACK") + list(chr(flag_frame)))
                        timeout=timeout+1/10



                        
            if flag_frame  == 65:
                flag_frame = 66
            else:
                if flag_frame  == 66:
                    flag_frame = 67
                else:
                    if flag_frame  == 67:
                        flag_frame = 65
            radio2.write(list("ACK") + list(chr(flag_frame)))
            for x in range(1, len(frame)):
                str_frame=str_frame + chr(frame[x])
            outputfile.write(str_frame)
            print(str_frame)
                

     #outputfile.close()



        
        
  
except KeyboardInterrupt:
    #outputfile.write(str_frame1)

    print("Interruption!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    outputfile.close()
    GPIO.output(23,0)
    GPIO.output(24,0)  
    GPIO.cleanup()



 








    
