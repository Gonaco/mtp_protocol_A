# coding=utf-8
from math import ceil
import zlib
import sys
import base64
import compression

def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()
def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print( "Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print( "Toc: start time not set")

filename_tx = "input - copia.txt"
#filename_tx = "Lorem ipsum.txt"
filename_tx_comp =  "input - copia_comp.txt"
filename_rx = "received.txt"

tic()
file_tx = open(filename_tx, 'rb')
uncompressed_text_tx = file_tx.read()
file_tx.close()

Compi_tx = compression.LZWCompressor()
data2tx = Compi_tx.compress(uncompressed_text_tx)

file_tx = open(filename_tx_comp, 'wb')
file_tx.write(data2tx)
file_tx.close()
toc()

print( "Text comprimit en bytes:  " + str(sys.getsizeof(data2tx)) + "B  cr(" + str(float(sys.getsizeof(uncompressed_text_tx))/float(sys.getsizeof(data2tx)))+ ")")


tic()
Compi_rx = compression.LZWCompressor()
uncompressed_text_rx = Compi_rx.uncompressFromFile(filename_tx_comp, filename_rx)

#file_rx = open(filename_rx, 'wb')
#file_rx.write(uncompressed_text_rx)
#file_rx.close()
toc()

print('Checking file:')
# print(Compi_rx.checkCompression(filename_tx, filename_rx))

