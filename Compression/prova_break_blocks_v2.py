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

#filename = "SampleTextFile_1000kb.txt"
#filename = "input-short.txt"
filename = "input - copia.txt"
filename_rx = "received.txt"


tic()
Compi_tx = compression.LZWCompressor()
Compi_tx.loadText(filename)
Compi_tx.compress()
compressed_data = Compi_tx.getCompressedData()
toc()


tic()
Compi_rx = compression.LZWCompressor()
Compi_rx.loadCompressedData(compressed_data)
Compi_rx.uncompress(filename_rx)
toc()