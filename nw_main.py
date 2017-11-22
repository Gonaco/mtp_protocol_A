import Net_main_functions.py as nw

ears, mouth = nw.setup()

timer = 5

while True:
    if (nw.listen(ears, timer)):
        nw.passive()
    else:
        print("Timeout")
