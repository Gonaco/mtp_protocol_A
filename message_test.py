import sys
import message_functions as m

def main(argv):

    # print ("\n"+argv[1])
    a = m.string2bits('a')
    print(a)
    head = a
    head = a[0] + m.string2bits('1')[0] + m.get_bin(50,32) # Cómo pasar de int a bin adecuadamente
    print (m.string2bits('1')[0][-2:])
    print(head)
    print(m.bits2string(head))
    print(m.string2bits(m.bits2string(head)))
    h = m.Header('a','00',50,'0')
    print (h)


if __name__ == "__main__":
    main(sys.argv)
