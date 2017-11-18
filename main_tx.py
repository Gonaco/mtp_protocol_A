import tx_main_functions as f

def main_tx(file):
    radio, radio2=f.setup()
    pipe = [1]
    f.synchronized(radio, radio2, pipe)
    id_last=f.transmit(radio, radio2, file)
    f.end_connection(radio, radio2, pipe, id_last)
    return 0

if __name__ == "__main__":
    main_tx()
