import tx_main_functions as f

def main_tx():
    file= open("tx_file.txt")
    radio, radio2=f.setup()
    pipe = [1]
    print(pipe)
    f.synchronized(radio, radio2, pipe)
    id_last=f.transmit(radio, radio2, file) # file is a reserved python word!!!!!
    f.end_connection(radio, radio2, pipe, id_last)
    return 0

if __name__ == "__main__":
    main_tx()
