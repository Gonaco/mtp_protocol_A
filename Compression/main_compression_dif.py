import zlib
import io
import numpy as np


def compressDiff(text):
    i = 0
    ii= 0
    num_comp=0
    #podem suposar que tot acaba amb \n?
    lines = text.split('\n')
    lines = lines[0:-1]
    line = lines[0]
    comps_res = np.array([], dtype=np.bool).reshape(0,len(line))
    for line in lines:
        char_line = np.array(list(line))
        i = i+1
        ii=0
        for line2 in lines:
            ii = ii+1
            if (ii>=i): #pendent a optimitzar per fer tots amb tots
                char_line2 = np.array(list(line2))
                comp_res = char_line==char_line2
                comps_res = np.vstack((comps_res,comp_res))
                print(line2)
                num_comp = num_comp +1
    print(num_comp)
    results = np.mean(comps_res, axis=0)
    where = np.where(results < 0.3)[0]
    where_str = where.astype(np.str)
    #enviar numericament millor?
    #optimitzar string?
    str_indices = ''
    for str in where_str:
        str_indices = str_indices + str + "¬"
    str_indices=str_indices[0:-1]
    str_send = ''

    for line in lines:
        char_line = np.array(list(line))
        char_line_send = char_line[where]
        for elem in char_line_send:
            str_send = str_send + elem
        str_send = str_send + '¬'
    to_tx = lines[0] + '\n&' + str_indices + '&' + str_send
    to_tx = to_tx[0:-1]

    return to_tx

def uncompressDiff(text):
    lines = text.split('&')

    original = lines[0]
    positions = lines[1].split('¬')
    lines = lines[2].split('¬')
    print("DECOMPRESSING!!!!")
    print(original)
    text_f = ''
    for line in lines:
        line = list(line)
        next_line = original
        next_line = list(next_line)
        i = 0
        for pos in positions:
            intpos = int(pos)
            next_line[intpos] = line[i]
            i = i + 1
        next_line = "".join(next_line)
        print(next_line)
        text_f = text_f + (next_line)
    print("fi programa")

    return text_f

file_input = io.open("input.txt", mode="r", encoding="utf-16")
text = file_input.read()
compressed_text = compressDiff(text)
print(compressed_text)
uncompressed_text = uncompressDiff(compressed_text)
print(text==uncompressed_text)



