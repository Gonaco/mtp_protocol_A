import rx_main_functions as rx
import time
import compression2

def tic():
    # Homemade version of Matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()


def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print( "Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print( "Toc: start time not set")

COMPRESSION = False


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
        tic()
        filename_origin = "RXfile_A.txt"
        filename_dest = "RXfile_A_uncomp.txt"
        Compi_rx = compression2.LZWCompressor()
        Compi_rx.uncompressFromFile(filename_origin, filename_dest)
        toc()

    return 0

if __name__ == "__main__":
    main_rx()
