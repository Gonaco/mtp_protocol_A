# https://es.wikipedia.org/wiki/Strategy_(patr%C3%B3n_de_dise%C3%B1o)#Python
# coding=utf-8
import compressionFunctions as cf
from math import ceil
import zlib
import sys
import base64
import abc


# Abstract class
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
    def uncompress(self, filename_rx):
        """Uncompress received data stream"""
        return

    @abc.abstractmethod
    def loadText(self, filename):
        """Load text file"""
        return

    @abc.abstractmethod
    def loadCompressedData(self, received_data):
        """"Load received data"""
        return

    @abc.abstractmethod
    def getCompressedData(self):
        """Get compresed data"""
        return

    @abc.abstractmethod
    def check(self, input_file):
        """Check if received text is correct"""
        return


# Inheriting from the above abstract class
class DifferentialCompressor(Compressor):

    uncompressed_text = None
    compressed_text = None

    def compress(self):
        # TODO
        return self.compressed_text

    def uncompress(self, filename_rx):
        # TODO
        return

    def loadText(self, filename):
        # TODO
        return

    def loadCompressedData(self, received_data):
        self.compressed_text = received_data
        return

    def getCompressedData(self):
        return self.compressed_text

    def check(self, input_file):
        # TODO
        return



# Inheriting from the above abstract class
class LZWCompressor(Compressor):

    uncompressed_text = None
    compressed_text = None

    num_blocks = 100;

    def setNumBlocks(self, num_blocks):
        self.num_blocks = num_blocks
        return

    def compress(self):
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
        return self.compressed_text

    def uncompress(self, filename_rx):
        received_data = base64.b64decode(self.compressed_text)

        received_filename = "received.txt"
        received_file = open(received_filename, 'w')

        for i in range(len(received_data)):
            received_text_block_compressed = received_data[i:]
            try:
                received_text_block_uncompressed = zlib.decompress(received_text_block_compressed)
            except:
                if i == 0:
                    print ("Can't uncompress if value is: " + str(i))
            else:
                received_file.write(received_text_block_uncompressed)

        received_file.close()
        return

    def loadText(self, filename):
        file = open(filename, 'r')
        self.uncompressed_text = file.read()
        file.close()
        return

    def loadCompressedData(self, received_data):
        self.compressed_text = received_data
        return

    def getCompressedData(self):
        return self.compressed_text

    def check(self, input_file):
        # TODO
        return









