# https://es.wikipedia.org/wiki/Strategy_(patr%C3%B3n_de_dise%C3%B1o)#Python

import abc


# Abstract class
class Compressor:
    # meta class is used to define other classes
    __metaclass__ = abc.ABCMeta

    #  decorator for abstract class
    @abc.abstractmethod
    def compress(self, input_text):
        """Compress the text we want to send"""
        return

    @abc.abstractmethod
    def uncompress(self, received_data):
        """Uncompress received data stream"""
        return

    @abc.abstractmethod
    def loadText(self, filename):
        """Load text file"""
        return

    @abc.abstractmethod
    def check(self, input_file):
        """Check if received text is correct"""
        return


# Inheriting from the above abstract class
class DifferentialCompressor(Compressor):

    def compress(self, input_text):
        # TODO
        return

    def uncompress(self, received_data):
        # TODO
        return

    def loadText(self, filename):
        # TODO
        return

    def check(self, input_file):
        # TODO
        return



# Inheriting from the above abstract class
class LZWCompressor(Compressor):
    def compress(self, input_text):
        # TODO
        return

    def uncompress(self, received_data):
        # TODO
        return

    def loadText(self, filename):
        # TODO
        return

    def check(self, input_file):
        # TODO
        return









