import tx_main_functions as f

def main_tx():
    archivo = open("Don_Quijoteaa.txt")
    radio, radio2=f.setup()
    pipe = [1]
    f.synchronized(radio, radio2, pipe)
    f.transmit(radio, radio2, archivo, pipe)
    f.end_connection(radio)
    return 0

if __name__ == "__main__":
    main_tx()
