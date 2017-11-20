# Compression and decompression of input text file

import zlib
import sys
import matplotlib.pyplot as plt
import numpy as np

def compressTextLZW( text ):
    "This compresses the text file using LZW"
    compressed_text = zlib.compress(text) #.encode("utf-8"))
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



# Introdice here name of the input text file
filename = "SampleTextFile_1000kb.txt"
#filename = "input - copia.txt"
#filename = "input.txt"




text = readTextFile(filename)
size_raw = sys.getsizeof(text)

compressed_text = compressTextLZW(text)
size_compressed = sys.getsizeof(compressed_text)

N = 100
size_compressed_array = []
length_of_text_array = []
compression_ratio_array = []
length_array = np.logspace(0, 6, N, endpoint=True)
length_array = length_array.astype(int)

for i in range(0, N):
    length = length_array[i] #100*i #int(size_raw*(i+1)/N)
    text = readTextFile2(filename, length)
    size_raw_i = sys.getsizeof(text)

    compressed_text = compressTextLZW(text)
    size_compressed_i = sys.getsizeof(compressed_text)
    size_uncompressed_i = sys.getsizeof(text)

    size_compressed_array.append(size_compressed_i)
    length_of_text_array.append(length)
    compression_ratio_array.append(size_uncompressed_i/size_compressed_i)

    print("Iteration ", i, ": Size of text is ", size_uncompressed_i, " B")


plt.plot(length_of_text_array, compression_ratio_array)
plt.show()

# print ("Size of raw text: ")
# print(size_raw, "B")
#
# print ("Size of compressed text: ")
# print(size_compressed, "B")
#
# print("Compression ratio:")
# print(size_raw/size_compressed)







