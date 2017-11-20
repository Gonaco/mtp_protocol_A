import zlib
import compressionFunctions as cf


filename = "input-short.txt"
#filename = "input - copia.txt"

num_lines = sum(1 for line in open(filename))
print("The text has, ", num_lines, " lines.")


# Read text file
file = open(filename, 'r')
text = file.read()

# Break 1MB text file to 100 10kB chunks
num_blocks = 100;
text_array = cf.breakTextInBlocks(text, num_lines, num_blocks)

# Create list with blocks, now compressed
text_array_compressed = []
for text_block in text_array
    text_block_compressed = zlib.compress(text_block)
    text_array_compressed.append( text_block_compressed )

# Create file to send
data_bits_to_send = cf.createDataBitsToSend( text_array_compressed )











