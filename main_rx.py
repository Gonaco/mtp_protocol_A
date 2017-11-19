import rx_main_functions as rx


def main_rx():
    radio, radio2 = rx.setup()
    pipe = [0]
    frame_received = rx.handshake(radio, radio2, pipe, 0)
    final_id = rx.receive(radio, radio2, pipe, frame_received)
    rx.handshake(radio, radio2, pipe, final_id)
    return 0

if __name__ == "__main__":
    main_rx()
