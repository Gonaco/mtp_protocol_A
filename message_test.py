import sys
import message_functions as m

def main(argv):

    # print ("\n"+argv[1])
    # a = m.string2bits('ab')
    # print(a)
    # head = a
    # head = a[0] + m.string2bits('1')[0] + m.get_bin(50,32) # Cómo pasar de int a bin adecuadamente
    # print (m.string2bits('1')[0][-2:])
    # print(head)
    # print(m.bits2string(head))
    # print(m.string2bits(m.bits2string(head)))

    # a = []
    # a.append('l')
    # a.append('j')

    # print(a)

    # Binary to Text
    # binary_data = b'I am text.'
    # text = binary_data.decode('utf-8')
    # print(text)

    # binary_data = bytes([65, 66, 67])  # ASCII values for A, B, C
    # text = binary_data.decode('utf-8')
    # print(text)
    
    # h = m.Header(97,3,2**31+55554,1)
    # print (h)
    # a = h.__str__()
    # print(h.header2byt())
    # j = m.Header()
    # j.extractHeader(a)
    # print(j)
    # k = m.Header(97,3,2**32-1,1)
    # print(k)
    # a = k.__str__()
    # print(k.header2byt())
    # j.extractHeader(a)
    # print(j)
    

    # p = m.SYNC(5000)
    # print(p)
    # k=p.header
    # print(k.header2byt())
    # print(p.packet2byt())
    # print(m.string2bits(p.payload))
    # h = m.Header()
    # h.extractHeader(p.__str__())
    # print(h)

    # rcv = m.Packet()
    # rcv.mssg2Pckt(p.__str__())
    # print(rcv)
    # print(rcv.getID())
    # print(rcv.payload)

    control = m.ControlFrame(m.D_TEAM)
    print(control)
    print(bin(ord(control.__str__())))
    rcv = []
    rcv.append(int(control.c2byt(),2))
    rcvc = m.ControlFrame()
    rcvc.mssg2Pckt(rcv)
    print(rcvc)

    data = m.DataFrame(m.B_TEAM, 0, "Hola peña")
    print(data)
    print(data.getPayload())
    print(data.d2byt())
    rcvd = m.DataFrame()
    n = []
    for i in range(0,len(data.d2byt())):
        n.append(int(data.d2byt()[i],2))
    rcvd.mssg2Pckt(n)
    print(rcvd)
    print(rcvd.getPayload())
    

if __name__ == "__main__":
    main(sys.argv)
