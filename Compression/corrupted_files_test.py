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
    file = open(filename, 'wb')
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
#filename = "SampleTextFile_1000kb.txt"
#filename = "input - copia.txt"
#filename = "input.txt"
filename = "input-short.txt"
filename_output = "output-short.txt"


# Compress file
text = readTextFile(filename)
compressed_text = compressTextLZW(text)

# Calculate file sizes
size_raw = sys.getsizeof(text)
size_compressed = sys.getsizeof(compressed_text)

# Corrupt file
compressed_text_corrupted = compressed_text[:len(compressed_text)//2+2]

# Uncompress file
uncompressed_text = uncompressTextLZW( compressed_text_corrupted )

# Write file
createTextFile( uncompressed_text, filename_output )







