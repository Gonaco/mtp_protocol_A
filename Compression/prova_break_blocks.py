# coding=utf-8
from math import ceil
import zlib
import sys
import base64

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


tic()

#filename = "SampleTextFile_1000kb.txt"
#filename = "input-short.txt"
filename = "input - copia.txt"

file = open(filename, 'r')
text = file.read()
lines = list(e + "\n" for e in text.split("\n")[:-1])
size_raw = sys.getsizeof(text)
file.close()

############################################################################################################### COMPRESS

# Break 1MB text file to 100 10kB chunks
num_blocks = 100;

num_lines = len(lines)
num_lines_per_block = int(ceil(float(num_lines) / float(num_blocks)))
num_lines_last_block = num_lines - (num_blocks - 1) * num_lines_per_block

block_text = []
entire_compression_data = None # First byte is a zero
for i in range(num_blocks):
    # Break entire text in small blocks
    first_line_of_block = i*num_lines_per_block
    if i==num_blocks-1:
        block_text = ''.join( lines[first_line_of_block:num_lines] )
    else:
        block_text = ''.join( lines[first_line_of_block:first_line_of_block+num_lines_per_block] )

    # Compress block and get size
    block_text_compressed = zlib.compress(block_text)
    block_text_compressed_size = sys.getsizeof(block_text_compressed)
    #print ( "Size of block " + str(i) + ": " + str(sys.getsizeof(block_text_compressed)) )

    # Put block data in big data stream
    if i==0:
        entire_compression_data = block_text_compressed
        block_text_compressed_size_first = block_text_compressed_size
        #entire_compression_data = block_text_compressed_size + block_text_compressed
    else:
        entire_compression_data = entire_compression_data + block_text_compressed
        #entire_compression_data = entire_compression_data + block_text_compressed_size + block_text_compressed


entire_compression_data_string = base64.b64encode(entire_compression_data)

toc()

# block_text_tx = block_text
# block_text_compressed_tx = zlib.compress(block_text_tx)
# block_text_compressed_64_tx = base64.b64encode(block_text_compressed_tx)
#
# block_text_compressed_64_rx = base64.b64decode(block_text_compressed_64_tx)
# block_text_rx = zlib.decompress(block_text_compressed_64_rx)

print( "num_blocks: " + str(num_blocks))
print( "num_lines:  " +str(num_lines))
print( "num_lines_per_block:  " + str(num_lines_per_block))
print( "num_lines_last_block: " + str(num_lines_last_block))
print( "\nAquest és el text:")
# print( block_text)
print( "Text comprimit en bytes:  " + str(sys.getsizeof(entire_compression_data))        + "B  cr(" + str(float(size_raw)/float(sys.getsizeof(entire_compression_data)))        + ")")
print( "Text comprimit en string: " + str(sys.getsizeof(entire_compression_data_string)) + "B  cr(" + str(float(size_raw)/float(sys.getsizeof(entire_compression_data_string))) + ")" + "\n\n")




############################################################################################################# UNCOMPRESS
tic()

received_data = base64.b64decode(entire_compression_data_string)

received_filename = "received.txt"
received_file = open(received_filename, 'w')

for i in range(len(received_data)):
    received_text_block_compressed = received_data[i:]
    try:
        received_text_block_uncompressed = zlib.decompress(received_text_block_compressed)
    except:
        if i==0:
            print ("Can't uncompress if value is: " + str(i))
    else:
        received_file.write(received_text_block_uncompressed)

received_file.close()

toc()