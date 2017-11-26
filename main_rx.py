import rx_main_functions as rx
import time

def main_rx():
    start = time.time()
    radio, radio2 = rx.setup()
    pipe = [0]
    frame_received = rx.handshake(radio, radio2, pipe, 0)
    final_id = rx.receive(radio, radio2, pipe, frame_received)
    end1 = time.time()
    diff = end1 - start
    print("Done sending the file! Exiting! It took: ", diff, " seconds")
    rx.handshake(radio, radio2, pipe, final_id)
    end2 = time.time()
    diff = end2 - start
    print("Done sending the file! Exiting! It took: ", diff, " seconds")
    return 0

if __name__ == "__main__":
    main_rx()
