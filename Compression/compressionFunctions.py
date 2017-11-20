import zlib
import sys
import matplotlib.pyplot as plt
import numpy as np

def compressTextLZW( text ):
    "This compresses the text file using LZW"
    compressed_text = zlib.compress(text)   #text.encode("utf-16"))
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

def breakTextInBlocks(filename, num_blocks):
    "This breaks a text in several blocks"
    lines = []  # Declare an empty list named "lines"
    with open(filename, 'rt') as in_file:  # Open file lorem.txt for reading of text data.
        for line in in_file:  # For each line of text store in a string variable named "line", and
            lines.append(line)  # add that line to our list of lines.
    text_array = []
    num_lines = len(lines)
    num_lines_per_block = num_lines//num_blocks
    num_lines_last_block = num_lines - (num_blocks-1)*num_lines_per_block


    return text_array

def createDataBitsToSend( text_array_compressed ):
    "This...."
    #TO_DO
    return data_bits_to_send
