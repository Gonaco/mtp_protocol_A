# Compression and decompression of input text file

import zlib
import sys
import matplotlib.pyplot as plt
import numpy as np

def compressTextLZW( text ):
    "This compresses the text file using LZW"
    compressed_text = zlib.compress(text.encode("utf-16"))
    # print(compressed_text)
    return compressed_text

def uncompressTextLZW( compressed_text ):
    "This uncompresses the text file using LZW"
    text = zlib.decompress(compressed_text)
    # print(text.decode("utf-16"))
    return text

def createTextFile( text, filename ):
    "This creates a .txt file containing the text input"
    file = open(filename, 'w')
    file.write(text)
    file.close()
    return

def readTextFile( filename ):
    "This reads a text file into a string"
    file = open(filename, 'r')
    text = file.read()
    return text

def readTextFile2( filename, length ):
    "This reads a text file into a string"
    file = open(filename, 'r')
    text = file.read(length)
    return text


def compressDiferential(text):
    "This compresses a text file type samle lines"
    lines = text.split('\n')
    i = 0
    ii = 0
    num_comp = 0
    #lines = file_input.readlines()
    line = lines[0]
    comps_res = np.array([], dtype=np.bool).reshape(0, len(line))
    for line in lines:
        line = line +'\n'
        char_line = np.array(list(line))
        i = i + 1
        ii = 0
        for line2 in lines:
            ii = ii + 1
            if (ii >= i):  # pendent a optimitzar per fer tots amb tots
                char_line2 = np.array(list(line2))
                comp_res = char_line == char_line2
                comps_res = np.vstack((comps_res, comp_res))
                print(line2)
                num_comp = num_comp + 1
    print(num_comp)
    results = np.mean(comps_res, axis=0)
    where = np.where(results < 0.3)[0]
    # enviar numericament millor?
    # optimitzar string?
    where_str = map(str, where)
    str_indices = ''
    for str in where_str:
        str_indices = str_indices + str + "¬"

    str_send = ''

    for line in lines:
        char_line = np.array(list(line))
        char_line_send = char_line[where]
        for elem in char_line_send:
            str_send = str_send + elem
        str_send = str_send + '¬'

    text_compressed = lines[1] + '&' + str_indices + '&' + str_send

    return text_compressed



# Introdice here name of the input text file
#filename = "SampleTextFile_1000kb.txt"
#filename = "input - copia.txt"
filename = "input.txt"




text = readTextFile(filename)
size_raw = sys.getsizeof(text)

compressed_text = compressTextLZW(text)
size_compressed = sys.getsizeof(compressed_text)

N = 100
size_compressed_array = []
length_of_text_array = []
compression_ratio_array = []

for i in range(0, N):
    length = 50*i #int(size_raw*(i+1)/N)
    text = readTextFile2(filename, length )
    size_raw_i = sys.getsizeof(text)

    compressed_text = compressDiferential(text) #compressTextLZW(text)
    size_compressed_i = sys.getsizeof(compressed_text)
    size_uncompressed_i = sys.getsizeof(text)

    size_compressed_array.append(size_compressed_i)
    length_of_text_array.append(length)
    compression_ratio_array.append(size_uncompressed_i/size_compressed_i)

    print("Iteration ", i, ": Size of text is ", size_uncompressed_i, " B")


plt.plot(length_of_text_array, compression_ratio_array, 'ro')
# plt.axis([0, 6, 0, 20])
plt.show()

# print ("Size of raw text: ")
# print(size_raw, "B")
#
# print ("Size of compressed text: ")
# print(size_compressed, "B")
#
# print("Compression ratio:")
# print(size_raw/size_compressed)







