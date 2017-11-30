import rx_main_functions as rx
import time
import compression2

COMPRESSION = True

def main_rx():
    start = time.time()
    radio, radio2 = rx.setup()
    pipe = [0]
    frame_received = rx.handshake(radio, radio2, pipe)
    rx.receive(radio, radio2, pipe, frame_received)
    end1 = time.time()
    diff = end1 - start
    print("Done sending the file! Exiting! It took: ", diff, " seconds")
    rx.handshake(radio, radio2, pipe)
    end2 = time.time()
    diff = end2 - start
    print("Done sending the file! Exiting! It took: ", diff, " seconds")

    if COMPRESSION:
        filename_origin = "something.txt"
        filename_dest = "something_else.txt"
        Compi_rx = compression2.LZWCompressor()
        Compi_rx.uncompressFromFile(filename_origin, filename_dest)

    return 0

if __name__ == "__main__":
    main_rx()
