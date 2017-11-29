# https://es.wikipedia.org/wiki/Strategy_(patr%C3%B3n_de_dise%C3%B1o)#Python
# coding=utf-8
from math import ceil
import zlib
import sys
import base64
import abc
import numpy as np
import io

# Abstract class


SEPA1 = chr(17)
SEPA2 = chr(18)


class Compressor:
    # meta class is used to define other classes
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def uncompressed_text(self):
        pass

    @abc.abstractproperty
    def compressed_text(self):
        pass

    #  decorator for abstract class
    @abc.abstractmethod
    def compress(self):
        """Compress the text we want to send"""
        return

    @abc.abstractmethod
    def uncompress(self):
        """Uncompress received data stream"""
        return

    def loadText(self, filename):
        print('\n-loadText-\n')
        file = io.open(filename, 'rb')
        self.uncompressed_text = file.read()
        file.close()
        return


    def writeDisk(self, filename):
        #print("\n-writeDisk-\n")

        file = io.open(filename, 'wb')
        file.write(self.uncompressed_text)
        file.close()
        return

    def checkCompression(self,filename1,filename2):
        file = io.open(filename1, 'rb')
        text1 = file.read()
        lines1 = text1.split('\n')
        lines1 = lines1[0:-1]
        file.close()
        file = io.open(filename2, 'rb')
        text2 = file.read()
        lines2 = text2.split('\n')
        lines2 = lines2[0:-1]
        file.close()
        i=0
        samelines = 0
        for line in lines1:
            if line !=lines2[i]:
                break
            i = i+1
        lines_equal = i
        return text1==text2,lines_equal

    def getCompressionRatio(self):
       return float(len(self.uncompressed_text))/len(self.compressed_text)


# Inheriting from the above abstract class
class DifferentialCompressor(Compressor):
    uncompressed_text = None
    compressed_text = None

    def compress(self):
        i = 0
        ii = 0
        num_comp = 0
        lines = self.uncompressed_text.split('\n')
        lines = lines[1:-1]
        line = lines[0]
        comps_res = np.array([], dtype=np.bool).reshape(0, len(line))
        for line in lines:
            char_line = np.array(list(line))
            i = i + 1
            ii = 0
            for line2 in lines:
                ii = ii + 1
                if (ii >= i):  # pendent a optimitzar per fer tots amb tots
                    char_line2 = np.array(list(line2))
                    comp_res = char_line == char_line2
                    comps_res = np.vstack((comps_res, comp_res))
                    num_comp = num_comp + 1
        print(num_comp)
        results = np.mean(comps_res, axis=0)
        where = np.where(results < 0.3)[0]
        where_str = where.astype(np.str)
        # enviar numericament millor?
        # optimitzar string?
        str_indices = ''
        for str in where_str:
            str_indices = str_indices + str + SEPA1
        str_indices = str_indices[0:-1]
        str_send = ''

        for line in lines:
            char_line = np.array(list(line))
            char_line_send = char_line[where]
            for elem in char_line_send:
                str_send = str_send + elem
            str_send = str_send + SEPA1
        to_tx = lines[0] + '\n'+SEPA2 + str_indices + SEPA2 + str_send
        to_tx = to_tx[0:-1]
        self.compressed_text = to_tx

        return self.compressed_text

    def uncompress(self):
        print('\n-uncompress-\n')
        lines = self.compressed_text.split(SEPA2)
        original = lines[0]
        positions = lines[1].split(SEPA1)
        lines = lines[2].split(SEPA1)
        print("DECOMPRESSING!!!!")
        text_f = ''
        for line in lines:
            line = list(line)
            next_line = original
            next_line = list(next_line)
            i = 0
            for pos in positions:
                intpos = int(pos)
                computed_len = len(line)
                if i>=computed_len or computed_len==0:
                    break
                next_line[intpos] = line[i]
                i = i + 1
            next_line = "".join(next_line)
            text_f = text_f + (next_line)
        print("Decompression ended!")
        self.uncompressed_text = text_f
        return self.uncompressed_text


    def loadCompressedData(self, received_data):
        self.compressed_text = received_data
        return


# Inheriting from the above abstract class
class LZWCompressor(Compressor):
    print("\n-LZWCompressor-\n")

    rx_filename = "default_receiver.txt"

    uncompressed_text = None
    compressed_text = None

    num_blocks = 100;
    current_byte = 0;

    def compress(self):
        #print('\n-compress-\n')
        lines = list(e + "\n" for e in self.uncompressed_text.split("\n")[:-1])
        num_lines = len(lines)
        num_lines_per_block = int(ceil(float(num_lines) / float(self.num_blocks)))
        num_lines_last_block = num_lines - (self.num_blocks - 1) * num_lines_per_block

        block_text = []
        entire_compression_data = None  # First byte is a zero
        for i in range(self.num_blocks):
            # Break entire text in small blocks
            first_line_of_block = i * num_lines_per_block
            if i == self.num_blocks - 1:
                block_text = ''.join(lines[first_line_of_block:num_lines])
            else:
                block_text = ''.join(lines[first_line_of_block:first_line_of_block + num_lines_per_block])

            # Compress block and get size
            block_text_compressed = zlib.compress(block_text)
            block_text_compressed_size = sys.getsizeof(block_text_compressed)
            # print ( "Size of block " + str(i) + ": " + str(sys.getsizeof(block_text_compressed)) )

            # Put block data in big data stream
            if i == 0:
                entire_compression_data = block_text_compressed
                block_text_compressed_size_first = block_text_compressed_size
                # entire_compression_data = block_text_compressed_size + block_text_compressed
            else:
                entire_compression_data = entire_compression_data + block_text_compressed
                # entire_compression_data = entire_compression_data + block_text_compressed_size + block_text_compressed

            self.compressed_text = base64.b64encode(entire_compression_data)
        ##print('Entire comp data: ' + entire_compression_data)
        return self.compressed_text

    def uncompress(self):
        #print('\n-uncompress-\n')

        received_data = base64.b64decode(self.compressed_text)

        ##print('Received data: ' + received_data)

        for i in range(self.current_byte, len(received_data)):
            received_text_block_compressed = received_data[i:]
            try:
                received_text_block_uncompressed = zlib.decompress(received_text_block_compressed)
            except:
                if i == 0:
                    print ("Can't uncompress if value is: " + str(i))
            else:
                if self.uncompressed_text==None:
                    #print("NONE")
                    self.uncompressed_text = received_text_block_uncompressed
                    with open(self.rx_filename, 'wb') as myfile:
                        myfile.write(self.uncompressed_text)
                else:
                    #print("i = " + str(i))
                    #print("received_text_block_uncompressed = " + received_text_block_uncompressed[:10])
                    self.current_byte = i
                    self.uncompressed_text = self.uncompressed_text + received_text_block_uncompressed
                    with open(self.rx_filename, 'a+b') as myfile:
                        myfile.write(received_text_block_uncompressed)
                #break
        ###print('Uncompressed text: ' + self.uncompressed_text)
        return self.uncompressed_text