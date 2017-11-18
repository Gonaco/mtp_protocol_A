import rx_main_functions as rx

def main():
    rx.setup()
    pipe = [0]
    rx.handshake(radio, radio2, pipe, 0)
    final_id = rx.receive(radio, radio2, pipe)
    rx.handshake(radio, radio2, pipe, final_id)
    return 0

if __name__ == "__main__":
    main_rx()